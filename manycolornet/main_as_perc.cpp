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
    std::stringstream idstring;
    idstring <<"_id" << rand()%9 << rand()%9 <<rand()%9 <<rand()%9 << ".json";
    std::stringstream ofname1;
    ofname1 <<"/tmp/AScolorpercolation_N"<<MCN.get_N();
    std::ofstream ofile(ofname1.str() + idstring.str());
    MCN.writeColorHistory(ofile);
    ofile.close();
    
    std::stringstream ofname2;
    ofname2 <<"/tmp/ASpercolation_N"<<MCN.get_N();
    std::ofstream ofile2(ofname2.str() + idstring.str());
    MCN.writeColorblindHistory(ofile2);
    ofile2.close();
    
    std::stringstream ofname3;
    ofname3 <<"/tmp/ASTwoCorepercolation_N"<<MCN.get_N();
    std::ofstream ofile3(ofname3.str() + idstring.str());
    MCN.writeTwoCoreHistory(ofile3);
    ofile3.close();
    
    return 0;
}
