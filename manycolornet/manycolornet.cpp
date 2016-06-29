#include <algorithm>
#include <fstream>
#include "manycolornet.h"
#include <assert.h>
#include <cstdlib>

ManyColorNet::ManyColorNet(uint N, uint C) :
N(N),C(C),S_color(N),adjacency_list(N),nodecolor(N),L_color(N),components(N),bfs_visited(N),randint(0,N-1)
{
    gen.seed(time(0));
    
    std::uniform_int_distribution<int> randcolor(0,C-1);
    
    std::generate(nodecolor.begin(), nodecolor.end(), [&](){return randcolor(gen);});
    std::fill(L_color.begin(),L_color.end(),1);
    
}

ManyColorNet::ManyColorNet(string node_list_fname, string edge_list_fname, int do_percolation) :adjacency_list(1),nodecolor(1)
{
    C=0;N=0;
    load_node_colors(node_list_fname);
    if(do_percolation){
      load_edges_to_container(edge_list_fname);
    }else{
      load_edges(edge_list_fname);  
    }
    N = adjacency_list.size();  
    S_color=N;  
    L_color.resize(N);
    components.resize(N);
    bfs_visited.resize(N);
    randint = std::uniform_int_distribution<uint>(0,N-1); 
    gen.seed(time(0));
    std::fill(L_color.begin(),L_color.end(),1);
    
}

void ManyColorNet::initialize_heterogeneous_colors(vector< double > rates)
{
  discrete_integer_distribution disc_int(&gen);
  disc_int.set_rates(rates);
  std::generate(nodecolor.begin(), nodecolor.end(), disc_int);
  std::fill(L_color.begin(),L_color.end(),1);
  C = rates.size();

  
}

void ManyColorNet::set_S_set(vector< int > new_S_set)
{
  S_set = std::move(new_S_set);
}

void ManyColorNet::set_T_set(vector< int > new_T_set)
{
  T_set = std::move(new_T_set);
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

void ManyColorNet::clear_network()
{
  adjacency_list.clear();
  adjacency_list.resize(N);
  num_links=0;
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


void ManyColorNet::load_edges_to_container(string edge_list_fname)
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
    edge_list.emplace_back(std::make_pair(sid,tid));
    
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

void ManyColorNet::shuffle_colors()
{
  std::uniform_int_distribution<uint> rand_node(0,N-1);
  int sweeps = 5;
  for(uint i = 0; i< sweeps*N; ++i)
    std::swap( nodecolor[rand_node(gen)],nodecolor[rand_node(gen)]);
  
}

void ManyColorNet::shuffle_links()
{
  vector<uint> edge_ends;
  for(auto & edge_pair : edge_list){
   edge_ends.push_back(edge_pair.first);
   edge_ends.push_back(edge_pair.second);
  }
  std::shuffle(edge_ends.begin(),edge_ends.end(),gen);
  std::uniform_int_distribution<uint> rand_edge_end(0,edge_ends.size()-1);
  int self_link_corrections = 0;
  for(uint i = 0; i<edge_ends.size()-1; i+=2){
    if(edge_ends[i] == edge_ends[i+1]){
      int this_id = edge_ends[i];
      int j = rand_edge_end(gen);
      while( edge_ends[j] == this_id 
	|| (j>0 && edge_ends[j-1] == this_id)
	|| (j<edge_ends.size()-1 && edge_ends[j+1] == this_id) )
      {
	  j = rand_edge_end(gen);
      }
      self_link_corrections++;
    }
    
  }
  int i = 0;
  for(auto & edge_pair : edge_list){
    edge_pair.first = edge_ends[i];
    edge_pair.second = edge_ends[i+1];
    i+=2;
  }
  std::cout << "corrected " <<self_link_corrections << " links.\n";
}


void ManyColorNet::intersection_update_L_color(int color)
{
    
    CA_BFS(color);
    auto LcbarIndexPair = std::max_element(component_size.begin(), component_size.end(), [](std::pair<uint,uint>& a, std::pair<uint,uint>&b){return a.second < b.second;});
#ifdef DEBUG
    std::cout << "|L_cbar("<<color<<")| = " << LcbarIndexPair->second;
#endif
    //jsonMap(component_size,std::cout);
    auto S_color0=S_color;
    uint giant_index = LcbarIndexPair->first;
    for(auto index_to_restore : bfs_double_counted[giant_index]){
	components[index_to_restore] = giant_index;
    }
#ifdef DEBUG
    if(std::count(components.begin(), components.end(), giant_index) != LcbarIndexPair->second){
	std::cerr << "Miscounted components!! : counted " <<  LcbarIndexPair->second << " found " <<
	std::count(components.begin(), components.end(), giant_index) << "!\n";
	//throw 1;
    }
#endif
    for(uint i=0; i<N; ++i){
	if(components[i] != giant_index){
	    if(L_color[i]){
		L_color[i] = 0;
		S_color--;
	    }
	}
    }
#ifdef DEBUG 
    std::cout << " ... restored "<<bfs_double_counted.size();
    std::cout << " ... reduced S_color by "<<S_color0 - S_color << " to " << S_color;
    std::cout << std::endl;
#endif
//     if(S_color > LcbarIndexPair->second){
//       
//     }
//     
    
}

void ManyColorNet::find_L_colorblind()
{
  CA_BFS(-1);
  auto giantIndexPair = std::max_element(component_size.begin(), component_size.end(), [](std::pair<uint,uint>& a, std::pair<uint,uint>&b){return a.second < b.second;});
  uint giant_index = giantIndexPair->first;
  uint S = giantIndexPair->second;
  numlinks_S_history.push_back(std::make_pair(num_links,S));

}

void ManyColorNet::find_L_twoCore()
{
  twoCore_BFS();
  auto giantIndexPair = std::max_element(component_size.begin(), component_size.end(), [](std::pair<uint,uint>& a, std::pair<uint,uint>&b){return a.second < b.second;});
  uint giant_index = giantIndexPair->first;
  uint StwoCore = giantIndexPair->second;
  numlinks_S_twoCore_history.push_back(std::make_pair(num_links,StwoCore));

}




void ManyColorNet::find_L_color()
{
    std::fill(L_color.begin(),L_color.end(),1);
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
    assert(S_color == std::count(L_color.begin(),L_color.end(),1));
   
    numlinks_Scolor_history.emplace_back(std::make_pair(num_links,S_color));
}

void ManyColorNet::find_L_color_ST()
{
      std::fill(L_color.begin(),L_color.end(),1);
      S_color=N;
      for(auto avoid_color_T : T_set){
	intersection_update_L_color(avoid_color_T);
      }
      assert(S_color == std::count(L_color.begin(),L_color.end(),1));
      for(auto avoid_color_S : S_set){
	for(int node_idx = 0; node_idx <N; node_idx++){
	  if( L_color[node_idx] && nodecolor[node_idx] == avoid_color_S){
	    L_color[node_idx]=0;
	    S_color--;
	  }
      }
      }
      numlinks_Scolor_history.emplace_back(std::make_pair(num_links,S_color));

}

void ManyColorNet::do_percolation(std::queue< uint > measuring_index_queue)
{
int stop_at = measuring_index_queue.front();
measuring_index_queue.pop();
std::shuffle(edge_list.begin(), edge_list.end(), gen);
for(int i=0; i<edge_list.size(); ++i){
  add_link(edge_list[i].first,edge_list[i].second);
  if(i >= stop_at){
      find_L_color();
      find_L_colorblind();
      find_L_twoCore();
      std::cout <<num_links << "  "  << S_color <<" \n";
      
      stop_at = measuring_index_queue.front();
      measuring_index_queue.pop();  
      if( measuring_index_queue.size() == 0)
	stop_at = edge_list.size();
  }

  
}
      find_L_color();
      find_L_colorblind();
      find_L_twoCore();
      std::cout <<num_links << "  "  << S_color <<" \n";
  
  
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
	component_size.push_back(std::make_pair(i,compsize));
	  
	}

	//std::cout << ", discovered " << compsize << "nodes.\n";
    }
}

bool ManyColorNet::twoCoreAlive(uint id)
{
    if(bfs_visited[id] == BFS::Black){
      return false;
    }

    if(adjacency_list[id].size() < 2){
      bfs_visited[id] = BFS::Black;
      return true;
    }
    int alive_neighbors = 0;
    for(auto  neighbor: adjacency_list[id]){
      if(bfs_visited[neighbor]!=BFS::Black)
	alive_neighbors++;
    }
    if(alive_neighbors <2){
      bfs_visited[id] = BFS::Black;
      return true;
    }
    return false;
}

void ManyColorNet::twoCore_BFS()
{
    std::fill(components.begin(),components.end(),-1);
    std::fill(bfs_visited.begin(), bfs_visited.end(),BFS::White);
      int twoCoreChangeCount=0,totalTwoCoreChanges=0;
  
    do{
      twoCoreChangeCount=0;
      for(uint i=0; i<N; i++){
      if(twoCoreAlive(i))
	twoCoreChangeCount++;
    }
      totalTwoCoreChanges+=twoCoreChangeCount;
    }while(twoCoreChangeCount);
   // std::cout << "TwoCore Removed " << totalTwoCoreChanges << "\n";
    while(!bfs_queue.empty()){ bfs_queue.pop();}
    component_size.clear();
    bfs_double_counted.clear();
    
    uint j,compsize=0;
    for(uint i=0; i<N; ++i){
	compsize=0;
	//if(nodecolor[i] == color )
	 // std::cout <<"Cannot start here: nodecolor["<<i<<"] == "<<color << "(cause it's " << nodecolor[i];
	if(bfs_visited[i] == BFS::White){
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
			bfs_queue.push(neighbor); // <-- only path that increases queue
			bfs_visited[neighbor] = BFS::Gray;
			components[neighbor] = i;
			compsize++;
		    }
		}
		bfs_visited[j]=BFS::Black;

	    }
	component_size.push_back(std::make_pair(i,compsize));
	  
	}

	//std::cout << ", discovered " << compsize << "nodes.\n";
    }
}

vector<vector<long>> ManyColorNet::count_same_color_links(long numTrials)
{
  vector<long> real_data(C);
  for(auto & edge_pair : edge_list){
      if(nodecolor[edge_pair.first] == nodecolor[edge_pair.second])
	real_data[nodecolor[edge_pair.first]]++;
  }
  vector<long> shuffled_data(C);
  for(long i =0; i<numTrials; i++){
    shuffle_colors();
    for(auto & edge_pair : edge_list){
      if(nodecolor[edge_pair.first] == nodecolor[edge_pair.second])
	shuffled_data[nodecolor[edge_pair.first]]++;
  }  
  }
  vector<long> color_freq(C);
  for(auto c: nodecolor){
    color_freq[c]++;
  }
  vector<vector<long>> output;
  for(long i=0;i<C; ++i){
   vector<long> row{real_data[i],shuffled_data[i],color_freq[i]};
    output.push_back(row);
  }
  return output;
}
