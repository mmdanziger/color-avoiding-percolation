#include <algorithm>
#include "manycolornet.h"
#include "jsonutils.hpp"

ManyColorNet::ManyColorNet(uint N, uint C) :
N(N),C(C),S_color(N),adjacency_list(N),nodecolor(N),L_color(N),components(N),bfs_visited(N),randint(0,N-1)
{
    gen.seed(time(0));
    std::uniform_int_distribution<int> randcolor(0,C-1);
    std::generate(nodecolor.begin(), nodecolor.end(), [&](){return randcolor(gen);});
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

void ManyColorNet::intersection_update_L_color(int color)
{
    
    CA_BFS(color);
    auto LcbarIndexPair = std::max_element(component_size.begin(), component_size.end(), [](std::pair<const uint,uint>& a, std::pair<const uint,uint>&b){return a.second < b.second;});
    uint giant_index = LcbarIndexPair->first;
    for(auto index_to_restore : bfs_double_counted[giant_index]){
	components[index_to_restore] = giant_index;
    }
    for(uint i=0; i<N; ++i){
	if(components[i] != giant_index){
	    if(L_color[i]){
		L_color[i] = false;
		S_color--;
	    }
	}
    }
	
    
}

void ManyColorNet::find_L_color()
{
    std::fill(L_color.begin(),L_color.end(),true);
    S_color=N;
    for(uint i=0; i<C; ++i){
	intersection_update_L_color(i);
    }
    numlinks_Scolor_history.emplace_back(std::make_pair(num_links,S_color));
}

template <typename stream_t> void ManyColorNet::writeHistory(stream_t& stream)
{
    jsonPairArray(numlinks_Scolor_history, stream);
}



void ManyColorNet::CA_BFS(int color)
{
    std::fill(components.begin(),components.end(),0);
    std::fill(bfs_visited.begin(), bfs_visited.end(),BFS::White);
    while(!bfs_queue.empty()){ bfs_queue.pop();}
    component_size.clear();
    bfs_double_counted.clear();
    
    uint j,compsize=0;
    for(uint i=0; i<N; ++i){
	compsize=0;
	if(bfs_visited[i] == BFS::White && nodecolor[i] != color ){
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
			bfs_double_counted[components[j]].push_back(j);
			components[neighbor] = i;
			compsize++;
		    }
   
		}
		bfs_visited[j]=BFS::Black;

	    }
	}
	component_size[i] = compsize;
    }
}
