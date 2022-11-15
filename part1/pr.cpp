// Copyright (c) 2009-2016 Craig Henderson
// https://github.com/cdmh/mapreduce

#include <boost/config.hpp>
#include <vector>
#include <chrono>
#if defined(BOOST_MSVC)
#pragma warning(disable : 4127)

// turn off checked iterators to avoid performance hit
#if !defined(__SGI_STL_PORT) && !defined(_DEBUG)
#define _SECURE_SCL 0
#define _HAS_ITERATOR_DEBUGGING 0
#endif
#endif

#include "mapreduce.hpp"

namespace page_rank
{

    struct Graph
    {
        int num_nodes;
        int num_edges;

        std::vector<std::pair<int, int>> edges;
        std::vector<int> out_degree;
        double *page_rank;

        Graph(std::string inp_file)
        {
            num_nodes = 0;

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

            out_degree.assign(num_nodes, 0);

            for (auto &edge : edges)
            {
                out_degree[edge.first]++;
            }
            // int c = 0;
            // for (int i = 0; i < num_nodes; i++)
            // {
            //     if (out_degree[i] == 0)
            //     {
            //         c += 1;
            //         std::cout << c << " " << " " << i << " " << num_nodes << std::endl;
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

    template <typename MapTask>
    class datasource : mapreduce::detail::noncopyable
    {
    public:
        typedef std::pair<int, int> value_type;

        datasource() : sequence_(0)
        {
        }

        bool const setup_key(typename MapTask::key_type &key)
        {
            key = sequence_++;
            return key < graph->num_edges;
        }

        bool const get_data(typename MapTask::key_type const &key, typename MapTask::value_type &value)
        {
            value.first = graph->edges[key].first;
            value.second = graph->edges[key].second;
            return true;
        }

    private:
        unsigned sequence_;
    };

    struct map_task : public mapreduce::map_task<int, std::pair<int, int>>
    {
        typedef std::pair<int, int> value_type;

        template <typename Runtime>
        void operator()(Runtime &runtime, key_type const &key, value_type const &value) const
        {
            runtime.emit_intermediate(value.second, graph->page_rank[value.first] / graph->out_degree[value.first]);
        }
    };

    struct reduce_task : public mapreduce::reduce_task<int, double>
    {

        template <typename Runtime, typename It>
        void operator()(Runtime &runtime, key_type const &key, It it, It ite) const
        {
            reduce_task::value_type result = 0;
            for (; it != ite; ++it)
                result += *it;
            runtime.emit(key, result);
        }
    };

    typedef mapreduce::job<page_rank::map_task,
                           page_rank::reduce_task,
                           mapreduce::null_combiner,
                           page_rank::datasource<page_rank::map_task>>
        job;

} // namespace page_rank

int main(int argc, char *argv[])
{
    mapreduce::specification spec;

    if (argc < 3)
    {
        std::cerr << "Usage: " << argv[0] << " <input_file> <output_file>" << std::endl;
        return 1;
    }

    std::string input_file(argv[1]);

    page_rank::graph = new page_rank::Graph(input_file);

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


        for (int i = 0; i < page_rank::graph->num_nodes; i++)
        {
            prev_avg += page_rank::graph->page_rank[i] / page_rank::graph->num_nodes;
            if (page_rank::graph->out_degree[i] == 0)
            {
                z_out_sum += page_rank::graph->page_rank[i] / page_rank::graph->num_nodes;
            }
        }


        page_rank::job::datasource_type datasource;
        page_rank::job job(datasource, spec);
        mapreduce::results result;

        job.run<mapreduce::schedule_policy::cpu_parallel<page_rank::job>>(result);

        std::swap(page_rank_, page_rank::graph->page_rank);

        for (int i = 0; i < page_rank::graph->num_nodes; i++)
        {
            page_rank::graph->page_rank[i] = 0.0;
        }

        for (auto it = job.begin_results(); it != job.end_results(); it++)
        {
            page_rank::graph->page_rank[it->first] = it->second;
        }

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

    } while (!done);

    delete[] page_rank_;

    std::ofstream file(argv[2]);
    for (int i = 0; i < page_rank::graph->num_nodes; i++)
    {
        file << i << " " << page_rank::graph->page_rank[i] << std::endl;
    }
    file.close();

    return 0;
}