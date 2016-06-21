#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <sstream>
#include <cstring>
#include "manycolornet.h"


using std::vector;





int main(int argc, char **argv) {
    srand(time(0));
    string data_dir = argc > 2 ? string(argv[2]) : "/home/micha/secret_mp/real_data/";
    int samples = argc >1? atoi(argv[1]) : 100;
    ManyColorNet MCN(data_dir + "caide-latest-complete-direct-vertex-colors-only.txt",data_dir + "caide-latest-complete-direct-edge-list.txt", 1);
    
    int linspace = 0;
        if(strstr(argv[0],"linspace"))
    {
      linspace=1;
    }
    std::queue<uint> measure_queue;

    //linear spacing sucks

    if(linspace){
      
    uint step = MCN.get_numlinks() / samples;
    for(uint i=0; i<MCN.get_numlinks(); i+=step)
	measure_queue.push(i);
    } else {
    //log spacing
    double maxpower  = log10(MCN.get_numlinks());
    double minpower  = log10(1.0/static_cast<double>(MCN.get_numlinks()));
    double step = (maxpower - minpower) / (samples - 1);
    int last_one=0;
    for(uint i=0; i<samples; ++i){
	int to_measure = round(pow10(minpower + i*step));
	if(to_measure > 0 && to_measure < MCN.get_numlinks() && to_measure != last_one){
	  measure_queue.push(to_measure);
	  last_one = to_measure;
	}
    }
    }
    std::string style_string = "";
    if(strstr(argv[0],"shuffle_colors"))
    {
      std::cout << "Shuffling colors ...\n";
      style_string += "_shuffled_colors";
      MCN.shuffle_colors();
    }
    if(strstr(argv[0],"shuffle_links"))
    {
      std::cout << "Shuffling links (degree preserving) ...\n";
      style_string += "_shuffled_links";
      MCN.shuffle_links();
    }
    

    MCN.do_percolation(measure_queue);
    
    /*WRITE OUTPUT */
    std::stringstream idstring;
    idstring <<"_id" << rand()%9 << rand()%9 <<rand()%9 <<rand()%9 << ".json";
    std::stringstream ofname;
    ofname <<"/tmp/AScolorpercolation"<< style_string <<"_N"<<MCN.get_N();
    std::ofstream ofile(ofname.str() + idstring.str());
    ofile << "{ \"Scolor\" : \n";
    MCN.writeColorHistory(ofile);
    ofile << ", \"S\" : \n";
    MCN.writeColorblindHistory(ofile);
    ofile << ", \"Stwocore\" : \n";
    MCN.writeTwoCoreHistory(ofile);
    ofile << "}\n";
    ofile.close();
    
    return 0;
}
