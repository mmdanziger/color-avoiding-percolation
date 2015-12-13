#include <vector>
#include <map>
#include <queue>
#include <random>
#include <string>

using std::vector;
using std::map;
using std::pair;
using std::string;

enum class BFS {Black, White, Gray};
class ManyColorNet {
  
private:
    uint N,C,num_links,S_color;
    vector< vector< uint > > adjacency_list;
    vector< int > nodecolor;
    vector <bool> L_color;
    vector <int> components;
    map <uint,uint> component_size;
    std::queue<uint> bfs_queue;
    vector <BFS> bfs_visited;
    map <uint,vector<uint>> bfs_double_counted;
    std::mt19937 gen;
    std::uniform_int_distribution<uint> randint;
    vector<std::pair<uint, uint> > numlinks_Scolor_history;
    
    
public:
    ManyColorNet(uint N, uint C);
    ManyColorNet(string node_list_fname, string edge_list_fname);
    void build_network_to_k(double k);
    void intersection_update_L_color(int color);
    void find_L_color();
    void CA_BFS(int color);
    void load_edges(string edge_list_fname);
    void load_node_colors(string node_list_fname);
    template<typename stream_t> void writeHistory(stream_t&  stream);
    template<typename stream_t> void writeLcolor(stream_t&  stream);
    template<typename stream_t> void writenodecolors(stream_t&  stream);

    void add_link(int sid, int tid);
    
};