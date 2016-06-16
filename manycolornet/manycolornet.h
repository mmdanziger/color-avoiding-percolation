#include <vector>
#include <map>
#include <queue>
#include <random>
#include <string>
#include <utility>
#include "jsonutils.hpp"

using std::vector;
using std::map;
using std::pair;
using std::string;
using upair = std::pair<uint,uint>;
enum class BFS {Black, White, Gray};

struct discrete_integer_distribution{
  int m_maxN;
  vector<double> rates;
  std::mt19937 *m_gen;
  discrete_integer_distribution(std::mt19937* gen){
    m_gen = gen;
    
  }
  void set_rates(vector<double> rates_to_set){
    rates.resize( rates_to_set.size() );
    std::copy(rates_to_set.begin(), rates_to_set.end(),rates.begin());
    double sum=0;
    for(auto r: rates){
      sum+=r;
    }
    for(auto &r: rates){
      r/=sum;
    }
    double last_val=0;
    for(auto &r: rates){
      r = r+last_val;
      last_val=r;
    }
    
  }
  int operator()(){
    double val = static_cast<double>((*m_gen)()) / static_cast<double>(std::mt19937::max());
    auto it = std::lower_bound(rates.begin(),rates.end(),val);
    return std::distance(rates.begin(),it);
  }
  
};

class ManyColorNet {
  
private:
    uint N,C,num_links,S_color;
    vector< vector< uint > > adjacency_list;
    vector< int > nodecolor;
    vector <int> L_color;
    vector <int> components;
    vector <int> S_set;
    vector <int> T_set;
    vector <upair> edge_list;
    vector <upair> component_size;
    std::queue<uint> bfs_queue;
    vector <BFS> bfs_visited;
    map <uint,vector<uint>> bfs_double_counted;
    std::mt19937 gen;
    std::uniform_int_distribution<uint> randint;
    vector<std::pair<uint, uint> > numlinks_Scolor_history;
    vector<std::pair<uint, uint> > numlinks_S_history;
    vector<std::pair<uint, uint> > numlinks_S_twoCore_history;
    
    
    
public:
    ManyColorNet(uint N, uint C);
    ManyColorNet(string node_list_fname, string edge_list_fname, int do_percolation =0 );
    void initialize_heterogeneous_colors(std::vector<double> rates);
    void set_S_set(vector<int> new_S_set);
    void set_T_set(vector<int> new_T_set);
    void build_network_to_k(double k);
    void clear_network();
    void intersection_update_L_color(int color);
    void find_L_color();
    void find_L_colorblind();
    void find_L_color_ST();
    void find_L_twoCore();
    uint get_S_color(){ return S_color;}
    void CA_BFS(int color);
    bool twoCoreAlive(uint id);
    void twoCore_BFS();
    void load_edges(string edge_list_fname);
    void load_edges_to_container(string edge_list_fname);
    void load_node_colors(string node_list_fname);
    void do_percolation(std::queue<uint> measuring_index_queue);
    template<typename stream_t> void writeColorHistory(stream_t&  stream);
    template<typename stream_t> void writeColorblindHistory(stream_t&  stream);
    template<typename stream_t> void writeTwoCoreHistory(stream_t&  stream);
    template<typename stream_t> void writeLcolor(stream_t&  stream);
    template<typename stream_t> void writenodecolors(stream_t&  stream);

    void add_link(int sid, int tid);
    const uint get_N() {return N;}
    const uint get_numlinks(){ return num_links > edge_list.size() ? num_links : edge_list.size();}
};


template <typename stream_t> 
void ManyColorNet::writeLcolor(stream_t& stream)
{
  stream << "[";
  for(uint i=0;i<N;++i){
    if (i>0)
      stream <<",\n";
    stream << "[" << i << ", "<< static_cast<int>(L_color[i]) << "]";
  }
  stream << "]\n";
  
}


template <typename stream_t> 
void ManyColorNet::writenodecolors(stream_t& stream)
{
  stream << "[";
  for(uint i=0;i<N;++i){
    if (i>0)
      stream <<",\n";
    stream << "[" << i << ", "<< nodecolor[i] << "]";
  }
  stream << "]\n";
  
}


template <typename stream_t> void ManyColorNet::writeColorHistory(stream_t& stream)
{
    jsonPairArray(numlinks_Scolor_history, stream);
}

template <typename stream_t> void ManyColorNet::writeColorblindHistory(stream_t& stream)
{
    jsonPairArray(numlinks_S_history, stream);
}

template <typename stream_t> void ManyColorNet::writeTwoCoreHistory(stream_t& stream)
{
    jsonPairArray(numlinks_S_twoCore_history, stream);
}