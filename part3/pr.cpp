#include <mpi.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <functional>
#include <chrono>
#include <thread>
#include <unordered_map>
#include "mapreduce.h"
#include "keyvalue.h"

#define LEADER_RANK 0

using namespace MAPREDUCE_NS;

namespace page_rank
{

    struct Graph
    {
        int num_nodes;
        int num_edges;

        std::vector<std::pair<int, int>> edges;
        std::vector<int> out_degree;
        double *page_rank;

        int mpi_comm_size;

        Graph(std::string inp_file, int mpi_comm_size)
        {
            num_nodes = 0;
            this->mpi_comm_size = mpi_comm_size;

            std::ifstream file(inp_file);
            if (!file)
            {
                std::cerr << "Error: unable to open file " << inp_file << std::endl;
                exit(1);
            }

            int src, dst;
            while (file >> src >> dst)
            {
                edges.push_back(std::make_pair(src, dst));
                num_nodes = std::max(num_nodes, std::max(src, dst) + 1);
            }

            file.close();

            out_degree.resize(num_nodes, 0);

            for (auto &edge : edges)
            {
                out_degree[edge.first]++;
            }

            // for (int i = 0; i < num_nodes; i++)
            // {
            //     if (out_degree[i] == 0)
            //     {
            //         for (int j = 0; j < num_nodes; j++)
            //         {
            //             edges.push_back(std::make_pair(i, j));
            //         }
            //         out_degree[i] = num_nodes;
            //     }
            // }
            num_edges = edges.size();
            page_rank = new double[num_nodes];
            for (int i = 0; i < num_nodes; i++)
            {
                page_rank[i] = 1.0 / num_nodes;
            }
        }
        ~Graph()
        {
            delete[] page_rank;
        }
    };

    Graph *graph;

    typedef std::pair<int, int> MAP_IN;

    typedef int REDUCE_KEY;
    typedef double REDUCE_VAL;

    void map_func(int my_rank, KeyValue *kv, void *graph)
    {
        Graph *g = (Graph *)graph;
        int num_nodes = g->num_nodes;
        int num_edges = g->num_edges;
        int mpi_comm_size = g->mpi_comm_size;

        int num_edges_per_proc = num_edges / mpi_comm_size;
        int start = my_rank * num_edges_per_proc;
        int end = (my_rank == mpi_comm_size - 1) ? num_edges : (my_rank + 1) * num_edges_per_proc;

        for (int i = start; i < end; i++)
        {
            auto edge = g->edges[i];
            double val = g->page_rank[edge.first] / g->out_degree[edge.first];
            kv->add((char *)&(edge.second), sizeof(int), (char *)&(val), sizeof(double));
        }
    }

    void reduce_func(char *key, int keybytes, char *multivalue, int nvalues, int *valuebytes, MAPREDUCE_NS::KeyValue *kv, void *ptr)
    {
        double sum = 0;
        for (int i = 0; i < nvalues; i++)
        {
            sum += *(double *)(multivalue + i * sizeof(double));
        }
        kv->add(key, keybytes, (char *)&sum, sizeof(double));
    }

    void scan_func(char *key, int keybytes, char *value, int valuebytes, void *ptr)
    {
        Graph *g = (Graph *)ptr;
        int node = *(int *)key;
        double val = *(double *)value;
        g->page_rank[node] = val;
    }

} // namespace page_rank

int main(int argc, char **argv)
{

    MPI_Init(&argc, &argv);

    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    if (argc < 3)
    {
        std::cerr << "Usage: " << argv[0] << " <input_file> <output_file>" << std::endl;
        return 1;
    }

    std::string input_file(argv[1]);

    page_rank::graph = new page_rank::Graph(input_file, world_size);

    double ALPHA = 0.85;
    double THRESHOLD = 0.00001;
    bool done = false;

    double *page_rank_ = new double[page_rank::graph->num_nodes];

    int itr = 0;

    auto start = std::chrono::high_resolution_clock::now();

    do
    {
        double prev_avg = 0.0;
        double z_out_sum = 0.0;

        if (world_rank == LEADER_RANK)
        {
            for (int i = 0; i < page_rank::graph->num_nodes; i++)
            {
                prev_avg += page_rank::graph->page_rank[i] / page_rank::graph->num_nodes;
                if (page_rank::graph->out_degree[i] == 0)
                {
                    z_out_sum += page_rank::graph->page_rank[i] / page_rank::graph->num_nodes;
                }
            }
        }

        std::unordered_map<page_rank::REDUCE_KEY, page_rank::REDUCE_VAL> results;

        MapReduce *mr = new MapReduce(MPI_COMM_WORLD);

        mr->verbosity = 0;

        mr->map(world_size, &page_rank::map_func, page_rank::graph);
        mr->collate(NULL);
        mr->reduce(&page_rank::reduce_func, NULL);

        if (world_rank == LEADER_RANK)
        {
            // memcpy(page_rank_, page_rank::graph->page_rank, sizeof(double) * page_rank::graph->num_nodes);
            std::swap(page_rank_, page_rank::graph->page_rank);
            for (int i = 0; i < page_rank::graph->num_nodes; i++)
            {
                page_rank::graph->page_rank[i] = 0.0;
            }
        }

        static_assert(LEADER_RANK == 0);
        mr->gather(1); // gather(i), gathers all the kvs into procs with id < i and procs with id >= i are left empty

        mr->scan(&page_rank::scan_func, page_rank::graph); // apply the results of reduce

        if (world_rank == LEADER_RANK)
        {
            double diff = 0.0;

            for (int i = 0; i < page_rank::graph->num_nodes; i++)
            {
                page_rank::graph->page_rank[i] += z_out_sum;
                page_rank::graph->page_rank[i] *= ALPHA;
                page_rank::graph->page_rank[i] += (1 - ALPHA) * prev_avg;
                diff += std::abs(page_rank::graph->page_rank[i] - page_rank_[i]);
            }

            auto end = std::chrono::high_resolution_clock::now();

            std::cout << "itr: " << itr << " diff: " << diff << ", ended at " << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() << "ms since start..." << std::endl;
            itr++;
            done = diff < THRESHOLD;

            // leader send done to all other processes
            for (int i = 0; i < world_size; i++)
            {
                if (i != LEADER_RANK)
                {
                    MPI_Send(&done, 1, MPI_C_BOOL, i, 0, MPI_COMM_WORLD);
                    if (!done)
                    {
                        // send page rank to all
                        MPI_Send(page_rank::graph->page_rank, page_rank::graph->num_nodes, MPI_DOUBLE, i, 0, MPI_COMM_WORLD);
                    }
                }
            }
        }
        else
        {
            // others receive done from leader
            MPI_Recv(&done, 1, MPI_C_BOOL, LEADER_RANK, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            if (!done)
            {
                // receive page rank from leader
                MPI_Recv(page_rank::graph->page_rank, page_rank::graph->num_nodes, MPI_DOUBLE, LEADER_RANK, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            }
        }

        delete mr;

    } while (!done);

    delete[] page_rank_;

    if (world_rank == LEADER_RANK)
    {
        std::ofstream file(argv[2]);
        for (int i = 0; i < page_rank::graph->num_nodes; i++)
        {
            file << i << " " << page_rank::graph->page_rank[i] << std::endl;
        }
        file.close();
    }

    MPI_Finalize();
    return 0;
}