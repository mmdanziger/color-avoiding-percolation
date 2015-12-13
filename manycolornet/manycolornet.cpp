#include <algorithm>
#include <fstream>
#include "manycolornet.h"
#include "jsonutils.hpp"
#include <assert.h>
#include <cstdlib>

ManyColorNet::ManyColorNet(uint N, uint C) :
N(N),C(C),S_color(N),adjacency_list(N),nodecolor(N),L_color(N),components(N),bfs_visited(N),randint(0,N-1)
{
    gen.seed(time(0));
    std::uniform_int_distribution<int> randcolor(0,C-1);
    std::generate(nodecolor.begin(), nodecolor.end(), [&](){return randcolor(gen);});
    std::fill(L_color.begin(),L_color.end(),true);
    
}

ManyColorNet::ManyColorNet(string node_list_fname, string edge_list_fname) :adjacency_list(1),nodecolor(1)
{
    C=0;N=0;
    load_node_colors(node_list_fname);
    load_edges(edge_list_fname);
    N = adjacency_list.size();    
    S_color=N;
    L_color.resize(N);
    components.resize(N);
    bfs_visited.resize(N);
    randint = std::uniform_int_distribution<uint>(0,N-1); 
    gen.seed(time(0));
    std::fill(L_color.begin(),L_color.end(),true);
    
}

void ManyColorNet::build_network_to_k(double k)
{
    uint s,t;
    while(num_links < N*k / 2){
	do{
	    s = randint(gen);
	    t = randint(gen);
	}while(s == t);
	if(std::find(adjacency_list[s].cbegin(), adjacency_list[s].cend(), t) == adjacency_list[s].cend()){
	    adjacency_list[s].push_back(t);
	    adjacency_list[t].push_back(s);
	    num_links++;
	}
    }
}

void ManyColorNet::add_link(int sid, int tid)
{
 // std::cout << "Adding link " <<sid << " -- " << tid << std::endl;
if(std::find(adjacency_list[sid].cbegin(), adjacency_list[sid].cend(), tid) == adjacency_list[sid].cend()){
	    adjacency_list[sid].push_back(tid);
	    adjacency_list[tid].push_back(sid);
	    num_links++;
	}
}


void ManyColorNet::load_edges(string edge_list_fname)
{
std::ifstream f(edge_list_fname);
string line,num_string;
uint sid,tid;
while(std::getline(f, line)) {
  if (line[0] == '#')
    continue;
  auto space_loc = std::find(line.begin(), line.end(), ' ');
  if (space_loc != line.end()){
    num_string = string(line.begin(), space_loc);
    sid = atoi(num_string.c_str());
    num_string = string(space_loc, line.end());
    tid = atoi(num_string.c_str());
    add_link(sid,tid);    
  }
  
}
  f.close();
}

void ManyColorNet::load_node_colors(string node_list_fname)
{
std::ifstream f(node_list_fname);
string line,num_string;
uint node_id,color_id;
map<int,int> nodecolormap;
while(std::getline(f, line)) {
  if (line[0] == '#')
    continue;
  auto space_loc = std::find(line.begin(), line.end(), ' ');
  if (space_loc != line.end()){
    num_string = string(line.begin(), space_loc);
    node_id = atoi(num_string.c_str());
    num_string = string(space_loc, line.end());
    color_id = atoi(num_string.c_str());
    color_id--;//because the data starts with color 1, not color 0
    C = std::max(C,static_cast<uint>(color_id));
    /*if(nodecolor.size() <= node_id){
      nodecolor.resize(node_id);
      adjacency_list.resize(node_id);
    }*/
    N = std::max(node_id,N);
    nodecolormap[node_id] = color_id;    
    //std::cout << "Coloring node " << node_id << " : " << color_id <<std::endl;
  }
  
  
}
nodecolor.resize(N);
adjacency_list.resize(N);
for(uint nid = 0; nid<N; nid++){
  auto nidit = nodecolormap.find(nid);
  if(nidit != nodecolormap.end()){
    nodecolor[nid] = nidit->second;
  }
}
  f.close();
}  






void ManyColorNet::intersection_update_L_color(int color)
{
    
    CA_BFS(color);
    auto LcbarIndexPair = std::max_element(component_size.begin(), component_size.end(), [](std::pair<const uint,uint>& a, std::pair<const uint,uint>&b){return a.second < b.second;});
    std::cout << "|L_cbar("<<color<<")| = " << LcbarIndexPair->second;
    //jsonMap(component_size,std::cout);
    auto S_color0=S_color;
    uint giant_index = LcbarIndexPair->first;
    for(auto index_to_restore : bfs_double_counted[giant_index]){
	components[index_to_restore] = giant_index;
    }   
    if(std::count(components.begin(), components.end(), giant_index) != LcbarIndexPair->second){
	std::cerr << "Miscounted components!! : counted " <<  LcbarIndexPair->second << " found " <<
	std::count(components.begin(), components.end(), giant_index) << "!\n";
	//throw 1;
    }
    for(uint i=0; i<N; ++i){
	if(components[i] != giant_index){
	    if(L_color[i]){
		L_color[i] = false;
		S_color--;
	    }
	}
    }
    
    std::cout << " ... restored "<<bfs_double_counted.size();
    std::cout << " ... reduced S_color by "<<S_color0 - S_color << " to " << S_color;
    std::cout << std::endl;
    if(S_color > LcbarIndexPair->second){
      
    }
    
    
}

void ManyColorNet::find_L_color()
{
    std::fill(L_color.begin(),L_color.end(),true);
    S_color=N;
    std::vector<uint> color_order(C);
    struct nplusone{
      int m_counter;
      nplusone(){m_counter=0;}
      uint operator()(){return m_counter++;}
    };

  std::generate(color_order.begin(), color_order.end(), nplusone());
  std::shuffle(color_order.begin(), color_order.end(),gen);
    //for(uint i=0; i<C; ++i){
  for(auto i: color_order){
	intersection_update_L_color(i);
    }
    assert(S_color == std::count(L_color.begin(),L_color.end(),true));
   
    numlinks_Scolor_history.emplace_back(std::make_pair(num_links,S_color));
}

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


template <typename stream_t> void ManyColorNet::writeHistory(stream_t& stream)
{
    jsonPairArray(numlinks_Scolor_history, stream);
}



void ManyColorNet::CA_BFS(int color)
{
    std::fill(components.begin(),components.end(),-1);
    std::fill(bfs_visited.begin(), bfs_visited.end(),BFS::White);
    while(!bfs_queue.empty()){ bfs_queue.pop();}
    component_size.clear();
    bfs_double_counted.clear();
    
    uint j,compsize=0;
    for(uint i=0; i<N; ++i){
	compsize=0;
	//if(nodecolor[i] == color )
	 // std::cout <<"Cannot start here: nodecolor["<<i<<"] == "<<color << "(cause it's " << nodecolor[i];
	if(bfs_visited[i] == BFS::White && nodecolor[i] != color ){
	  //  std::cout << "("<<color <<")Starting search from " << i << " of color " << nodecolor[i];// <<std::endl;
	    bfs_queue.push(i);
	    bfs_visited[i]=BFS::Gray;
	    components[i]=i;
	    compsize++;
	    while(!bfs_queue.empty()){
		j=bfs_queue.front();
		bfs_queue.pop();
		for(auto neighbor : adjacency_list[j]){
		    if(bfs_visited[neighbor] == BFS::White){
			if(nodecolor[neighbor] != color){
			    bfs_queue.push(neighbor); // <-- only path that increases queue
			    bfs_visited[neighbor] = BFS::Gray;
			    components[neighbor] = i;
			    compsize++;
			} else { // encountered color to avoid, include it in component but do not follow
			    bfs_visited[neighbor] = BFS::Black;
			    components[neighbor] = i;
			    compsize++;
			} 
		    }
		    if(bfs_visited[neighbor] == BFS::Black && nodecolor[neighbor] == color && components[neighbor] != i){ // encountered color node that has already been counted
			bfs_double_counted[components[neighbor]].push_back(neighbor);
			components[neighbor] = i;
			compsize++;
		    }
   
		}
		bfs_visited[j]=BFS::Black;

	    }
	}
	component_size[i] = compsize;
	//std::cout << ", discovered " << compsize << "nodes.\n";
    }
}
