#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/detail/incremental_components.hpp>
#include <boost/graph/incremental_components.hpp>
#include <boost/unordered_set.hpp>
#include <boost/pending/disjoint_sets.hpp>
#include <boost/multi_index_container.hpp>
#include <boost/multi_index/member.hpp>
#include <boost/multi_index/ordered_index.hpp>
#include <vector>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <stdexcept>
#include <exception>
using std::pair;
using std::vector;
using std::logic_error;
typedef boost::adjacency_list <boost::vecS, boost::vecS, boost::undirectedS> Graph;
typedef boost::graph_traits<Graph>::vertex_descriptor Vertex;
typedef boost::graph_traits<Graph>::edge_descriptor Edge;
typedef boost::graph_traits<Graph>::vertices_size_type VertexIndex;
typedef VertexIndex* Rank;
typedef Vertex* Parent;
typedef boost::disjoint_sets<Rank, Parent> DSet;


//Function to write jsonArray from any iterable to any stream (file or cout)
template <typename T, typename Stream> void  jsonArray(T toPrint, Stream &stream, double Norm=1)
{
    stream<<"[";
    bool firstVal=true;
    for( auto val: toPrint)
    {
        if (!firstVal)
            stream<<",";
        firstVal=false;

        if(Norm == 1)
            stream << val;
        else
            stream <<val / Norm;

    }
    stream<<"]";
    stream.flush();
}  

int randint(unsigned N){
 return rand()%N;   
}

//Necessary for constructing a boost multi_index_container keeping a running tally of GC sizes and ids
struct id {};
struct size {};
struct component_pair{
    int id;
    int size;
component_pair(int id_, int size_):id(id_),size(size_){};  
};

typedef boost::multi_index_container<
component_pair,
boost::multi_index::indexed_by<
boost::multi_index::ordered_unique<
    boost::multi_index::tag<id>,  BOOST_MULTI_INDEX_MEMBER(component_pair,int,id)>,
boost::multi_index::ordered_non_unique<
    boost::multi_index::tag<size>,BOOST_MULTI_INDEX_MEMBER(component_pair,int,size)> >
> CompSet;

//Functor to generate edges, perhaps not the best design pattern but effective
struct makeEdge{
    //Members:
    std::string mType;
    unsigned mN;
    //Constructor:
    makeEdge(std::string type,unsigned N):mType(type),mN(N){};   
    //Functor operator
    std::pair<int,int> operator ()(){
        int x,y;
        if (mType == "random"){
            do{
            x = randint(mN);
            y = randint(mN);
            }while(y == x);
            return x>y? std::make_pair(y,x) : std::make_pair(x,y);
        }
        else{
            throw logic_error("Undefined topology");
        }
    }
};


class ColorNet{
private:
        unsigned N;
        unsigned nColors;
        std::vector<int> nodeColors;
        std::vector<pair<int,int> > antiColorGiant;
        std::vector<int> mutualGC;
        Graph G;
        std::vector<std::pair<int,int>> edgeVector;
        std::vector<DSet> antiColorDsets;
        std::vector<std::vector<VertexIndex> > antiColorParent;
        std::vector<std::vector<Vertex> > antiColorRank;
        std::vector<CompSet> antiColorComponentSets;
        std::vector<long unsigned> gcHistory;
        std::string outputFileName;
        int verbosity;
public:
        ColorNet(unsigned int N, unsigned int nColors);
        void setNodeColors();
        void setFileName(std::string fname);
        void blackOutColor(int colorNumber);
        void buildAntiColorComponents();
        std::pair<int,int> getMaxPair( vector< int > components, int num);
        void buildMutualGC();
        void buildNetwork();
        long unsigned getMutualGC();
        void incrementalComponents(double fromK, double toK, int link_res);
        void buildEdgeVector(double toK);
        void initializeDSets();
        void mergeComponents(int color, int u, int v);
        long unsigned getMutualGCFromDSets();
        void writeResults();

};
//TODO: Add method which adds one link at a time and keeps modifying the giant component, like the algorithm Newman showed
ColorNet::ColorNet(unsigned int N, unsigned int nColors):N(N),nColors(nColors),nodeColors(N),G(N)
{
    setNodeColors();
    buildNetwork();
    verbosity=0;
}

void ColorNet::buildNetwork()
{
//For now, we don't do anything here.
}


void ColorNet::setNodeColors()
{
    std::generate(nodeColors.begin(), nodeColors.end(), [this](){return randint(nColors);});
    //jsonArray(nodeColors,std::cout);
}



void ColorNet::buildEdgeVector(double toK)
{

unsigned to_links = N*toK/2;
boost::unordered_set<std::pair<int,int>> edge_list; 
while( edge_list.size() < to_links){
    edge_list.insert(makeEdge("random",N)());   
}
//unordered_set is liable to have a non random ordering dependent on the hash function (right?)
edgeVector = std::vector<std::pair<int,int>>(edge_list.begin(), edge_list.end());

std::random_shuffle(edgeVector.begin(),edgeVector.end());
//std::cout<<"Generated "<<edgeVector.size() <<" edges\n";
}

void ColorNet::initializeDSets()
{
// try{    
// antiColorRank.resize(nColors);
// antiColorParent.resize(nColors);
// antiColorComponentSets.resize(nColors);
// }catch( std::exception &e){
//  std::cerr<<"Failed to resize antiColor* vectors.\n";   
// }
    antiColorGiant.resize(nColors);
for(unsigned color_index = 0; color_index<nColors; color_index++){
    antiColorRank.push_back(std::vector<Vertex>(N));
    antiColorParent.push_back(std::vector<VertexIndex>(N));
    antiColorComponentSets.push_back(CompSet());
    antiColorDsets.push_back(DSet(&antiColorRank[color_index][0], &antiColorParent[color_index][0]));
    for(unsigned j=0; j<N; ++j){
        antiColorDsets[color_index].make_set(j);
        if (nodeColors[j] != color_index){
           antiColorComponentSets[color_index].insert(component_pair(j,1));
        }
    }
}
}

void ColorNet::mergeComponents(int color, int u, int v)
{
     auto it_u = antiColorComponentSets[color].get<id>().find(u);
     int size1 = it_u->size;
     auto it_v = antiColorComponentSets[color].get<id>().find(v);
     int size2 =it_v->size;
     antiColorDsets[color].link(u,v);
     auto w = antiColorDsets[color].find_set(u);
     auto new_comp_it = antiColorComponentSets[color].get<id>().find(w);
     auto new_comp = *new_comp_it;
     new_comp.size = size1+size2;
     antiColorComponentSets[color].replace(new_comp_it,new_comp);
     if(u == w)
         antiColorComponentSets[color].erase(it_v);
     else
         antiColorComponentSets[color].erase(it_u);
}


void ColorNet::incrementalComponents(double fromK, double toK, int link_res)
{
    
long to_links = toK*N/2;
long from_links = toK*N/2;
long link_count = 0;
buildEdgeVector(toK);

try{
initializeDSets();
}catch(std::exception &e){
    std::cerr<< "Failed to initialize DSets:\n";
    std::cerr<<e.what()<<std::endl;
}
int s,t,sColor,tColor;
gcHistory.resize(to_links);
while(link_count < to_links ){
    s = edgeVector[link_count].first;
    t = edgeVector[link_count].second;
    boost::add_edge(s,t,G);
    sColor = nodeColors[s];
    tColor = nodeColors[t];
    for(int color=0; color<nColors; color++){
        if (color == sColor || color == tColor)
            continue;
        int u = antiColorDsets[color].find_set(s);
        int v = antiColorDsets[color].find_set(t);
        if(u!=v){
            mergeComponents(color,u,v);
        }
    }
    gcHistory[link_count]  = getMutualGCFromDSets();
    //std::cout<<gcHistory[link_count]<<std::endl;
    link_count++;    
}


    
    
}

long unsigned ColorNet::getMutualGCFromDSets()
{
    mutualGC.resize(N);
    for(unsigned color=0; color<nColors; color++){
        auto it = antiColorComponentSets[color].get<size>().rbegin();
        if (it == antiColorComponentSets[color].get<size>().rend())
            return 0;
        antiColorGiant[color] = std::make_pair(it->id,it->size);
        
        if(verbosity >1)
        {
            std::cout<<"S_"<<color<<" = "<< antiColorGiant[color].second<<"\n";
            vector<int> temp_comps(N);
            for(unsigned i=0; i<N; i++)
                temp_comps[i] = antiColorDsets[color].find_set(i) == antiColorGiant[color].first? 1 : 0;
            jsonArray(temp_comps,std::cout);
        }
}
    bool inMutualGC=false;
    for(unsigned node=0; node<N; node++){
        inMutualGC=true;
        int this_color = nodeColors[node];
        for(unsigned color=0; color<nColors; color++){
            if (color == this_color)
                continue;
            if (antiColorDsets[color].find_set(node)!= antiColorGiant[color].first){
                inMutualGC=false;
                break;
            }
        }
        if (inMutualGC){
            inMutualGC=false; 
            typename boost::graph_traits < Graph >::adjacency_iterator vi, vi_end;
            for (boost::tie(vi, vi_end) = boost::adjacent_vertices(node, G); vi != vi_end; ++vi){
                if (antiColorDsets[this_color].find_set(*vi) == antiColorGiant[this_color].first){
                    inMutualGC=true;
                    break;
                }
            }
        }

        mutualGC[node]=inMutualGC? 1 : 0;
       
    }
return getMutualGC();
    
}



void ColorNet::setFileName(std::string fname){

    outputFileName=fname;
    
}

void ColorNet::writeResults()
{
std::ofstream outputFile(outputFileName.c_str());
outputFile << "{\"N\":"<<N<<",\n";
outputFile << "\"Nc\":"<<nColors<<",\n";
outputFile << "\"S_color\":";
jsonArray(gcHistory,outputFile);
outputFile << "}\n";
outputFile.close();

}


long unsigned ColorNet::getMutualGC()
{
    if (mutualGC.size() != N)
        throw logic_error("You need to build the mutual GC before you can view it!");
    return std::accumulate(mutualGC.cbegin(),mutualGC.cend(),0);
}
