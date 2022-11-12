#include <mpi.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <functional>
#include <chrono>
#include <thread>
#include <unordered_map>



#define LEADER_RANK 0


template <typename T, typename S>
void map_and_shuffle(int my_rank, std::vector<T> &data, int comm_size, std::function<S(T)> map_func, std::function<int(S)> partition_func, std::vector<S> &results)
{
    int chunk_size = data.size() / comm_size;
    int start = my_rank * chunk_size;
    int end = (my_rank + 1) * chunk_size;
    if (my_rank == comm_size - 1)
    {
        end = data.size();
    }
    std::vector<std::vector<S>> mapped_results(comm_size);
    for (int i = start; i < end; i++)
    {
        S mapped = map_func(data[i]);
        int partition = partition_func(mapped);
        mapped_results[partition].push_back(mapped);
    }


    MPI_Request request = MPI_REQUEST_NULL;

    for (int i = 0; i < comm_size; i++)
    {
        if (i == my_rank)
        {
            for (S res : mapped_results[i])
            {
                results.push_back(res);
            }
        }
        else
        {
            long long size = mapped_results[i].size(); // send my size

            // assumes all processes have the same endianness
            MPI_Isend(&size, 1, MPI_LONG_LONG, i, 0, MPI_COMM_WORLD, &request);

            MPI_Irecv(&size, 1, MPI_LONG_LONG, i, 0, MPI_COMM_WORLD, &request); // recv my size

            MPI_Wait(&request, MPI_STATUS_IGNORE);

            S *recv_data = new S[size];

            MPI_Isend(mapped_results[i].data(), mapped_results[i].size() * sizeof(S), MPI_BYTE, i, 0, MPI_COMM_WORLD, &request); // send my data

            MPI_Irecv(recv_data, size * sizeof(S), MPI_BYTE, i, 0, MPI_COMM_WORLD, &request); // recv my data

            MPI_Wait(&request, MPI_STATUS_IGNORE);

            for (int j = 0; j < size; j++)
            {
                results.push_back(recv_data[j]);
            }

            delete[] recv_data;

        }
    }
}

template <typename K, typename V>
void reduce(std::vector<std::pair<K,V>> &map_results, std::function<V(V,V)> reduce_func, std::unordered_map<K, V> &results) 
{

    for (auto &pair : map_results)
    {
        results[pair.first] = reduce_func(results[pair.first], pair.second);
    }
}



template <typename K, typename V>
void share_and_collect_reduce_results(int my_rank, int comm_size, std::unordered_map<K,V>& results) {
    if (my_rank != LEADER_RANK) {
        std::vector<std::pair<K,V>> results_vector;
        for (auto &pair : results) {
            results_vector.push_back(pair);
        }
        long long size = results_vector.size();
        MPI_Send(&size, 1, MPI_LONG_LONG, LEADER_RANK, 0, MPI_COMM_WORLD);
        MPI_Send(results_vector.data(), results_vector.size() * sizeof(std::pair<K,V>), MPI_BYTE, LEADER_RANK, 0, MPI_COMM_WORLD);
    }
    else {
        // Leader collects
        for (int i = 0; i < comm_size; i++) {
            if (i != my_rank) {
                long long size;
                MPI_Recv(&size, 1, MPI_LONG_LONG, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                std::pair<K,V> *recv_data = new std::pair<K,V>[size];

                MPI_Recv(recv_data, size * sizeof(std::pair<K,V>), MPI_BYTE, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                for (int j = 0; j < size; j++)
                {
                    results[recv_data[j].first] = recv_data[j].second;
                }
                delete[] recv_data;
            }
        }
    }
}


template <typename MAP_IN, typename REDUCE_KEY, typename REDUCE_VAL>
void map_reduce_job(int my_rank, int comm_size, std::vector<MAP_IN> &data, std::function<std::pair<REDUCE_KEY, REDUCE_VAL>(MAP_IN)> map_func, 
    std::function<int(std::pair<REDUCE_KEY, REDUCE_VAL>)> partition_func, std::function<REDUCE_VAL(REDUCE_VAL, REDUCE_VAL)> reduce_func, 
    std::unordered_map<REDUCE_KEY, REDUCE_VAL> &results)
{
    std::vector<std::pair<REDUCE_KEY, REDUCE_VAL>> map_results;
    map_and_shuffle<MAP_IN, std::pair<REDUCE_KEY, REDUCE_VAL>> (my_rank, data, comm_size, map_func, partition_func, map_results);
    reduce(map_results, reduce_func, results);
    share_and_collect_reduce_results(my_rank, comm_size, results);
}



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

            for (int i = 0; i < num_nodes; i++)
            {
                if (out_degree[i] == 0)
                {
                    for (int j = 0; j < num_nodes; j++)
                    {
                        edges.push_back(std::make_pair(i, j));
                    }
                    out_degree[i] = num_nodes;
                }
            }
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


    static std::pair<REDUCE_KEY, REDUCE_VAL> map_func(MAP_IN edge)
    {
        return std::make_pair(edge.second, graph->page_rank[edge.first] / graph->out_degree[edge.first]);
    }

    static int partition_func(std::pair<REDUCE_KEY, REDUCE_VAL> pair)
    {
        return pair.first % graph->mpi_comm_size;
    }

    static REDUCE_VAL reduce_func(REDUCE_VAL a, REDUCE_VAL b)
    {
        return a + b;
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

    double* page_rank_ = new  double[page_rank::graph->num_nodes];

    int itr = 0;

    auto start = std::chrono::high_resolution_clock::now(); 
    do {
        std::unordered_map<page_rank::REDUCE_KEY, page_rank::REDUCE_VAL> results;
        map_reduce_job<page_rank::MAP_IN, page_rank::REDUCE_KEY, page_rank::REDUCE_VAL>(world_rank, world_size, page_rank::graph->edges, 
                        page_rank::map_func, page_rank::partition_func, page_rank::reduce_func, results);

        if (world_rank == LEADER_RANK) {
            memcpy(page_rank_, page_rank::graph->page_rank, sizeof(double) * page_rank::graph->num_nodes);

            double prev_avg = 0.0;

            for (int i = 0; i < page_rank::graph->num_nodes; i++) {
                prev_avg += page_rank::graph->page_rank[i] / page_rank::graph->num_nodes;
            }

            for (auto &result : results) {
                page_rank::graph->page_rank[result.first] = result.second;       
            }

            double diff = 0.0;

            for (int i = 0; i < page_rank::graph->num_nodes; i++) {
                page_rank::graph->page_rank[i] *= ALPHA;
                page_rank::graph->page_rank[i] += (1 - ALPHA) *  prev_avg;
                diff += std::abs(page_rank::graph->page_rank[i] - page_rank_[i]);
            }
            
            auto end = std::chrono::high_resolution_clock::now(); 

            std::cout << "itr: " << itr << " diff: " <<  diff << ", ended at " << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() << "ms since start..." << std::endl;
            itr++;
            done = diff < THRESHOLD;

            // leader send done to all other processes
            for (int i = 0; i < world_size; i++) {
                if (i != LEADER_RANK) {
                    MPI_Send(&done, 1, MPI_C_BOOL, i, 0, MPI_COMM_WORLD);
                    if (!done) {
                        //send page rank to all
                        MPI_Send(page_rank::graph->page_rank, page_rank::graph->num_nodes, MPI_DOUBLE, i, 0, MPI_COMM_WORLD);
                    }
                }
            }
        }
        else {
            // others receive done from leader
            MPI_Recv(&done, 1, MPI_C_BOOL, LEADER_RANK, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            if (!done) {
                // receive page rank from leader
                MPI_Recv(page_rank::graph->page_rank, page_rank::graph->num_nodes, MPI_DOUBLE, LEADER_RANK, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            }
        }


    } while (!done);

    delete[] page_rank_;


    if (world_rank == LEADER_RANK) {
        std::ofstream file(argv[2]);
        for (int i = 0; i < page_rank::graph->num_nodes; i++) {
            file << i << " " << page_rank::graph->page_rank[i] << std::endl;
        }
        file.close();
    }



    MPI_Finalize();
    return 0;
}