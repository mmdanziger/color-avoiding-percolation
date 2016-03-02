#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <sstream>
#include "manycolornet.h"


using std::vector;





int main(int argc, char **argv) {
    srand(time(0));
    string data_dir = argc > 1 ? string(argv[1]) : "/home/micha/secret_mp/real_data/";
    int samples = argc >2? atoi(argv[2]) : 100;
    ManyColorNet MCN(data_dir + "caide-latest-complete-direct-vertex-colors-only.txt",data_dir + "caide-latest-complete-direct-edge-list.txt", 1);
    
    std::queue<uint> measure_queue;
    MCN.get_N();
    uint step = MCN.get_numlinks() / samples;
    for(uint i=0; i<MCN.get_numlinks(); i+=step)
	measure_queue.push(i);
    MCN.do_percolation(measure_queue);
    
    /*WRITE OUTPUT */
    std::stringstream ofname;
    
    ofname <<"/tmp/ASpercolation_N"<<MCN.get_N() <<"_id"<< rand()%9 << rand()%9 <<rand()%9 <<rand()%9 <<".json";    
    std::ofstream ofile(ofname.str());
    MCN.writeHistory(ofile);
    ofile.close();
    return 0;
}
