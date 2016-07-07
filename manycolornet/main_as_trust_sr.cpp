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
    string data_dir = argc > 3 ? string(argv[3]) : "/home/micha/secret_mp/real_data/";
    int top_k = argc > 1? atoi(argv[1]) : 20;
    float p = argc > 2? atof(argv[2]) : 1;
    std::cout << p << "\n";
    ManyColorNet MCN(data_dir + "caide-latest-complete-direct-vertex-colors-only.txt",data_dir + "caide-latest-complete-direct-edge-list.txt", 1);
    int Scol;
    MCN.load_network_from_edgelist_to_p(1);
    std::stringstream ofname;
    ofname << "/tmp/AS_SR_top_"<<top_k<<"_p"<<p<<".txt";
    std::ofstream ofile(ofname.str());
    std::vector< vector<int> > most_common_colors = MCN.get_colors_by_freq();
    
    for(int S = 0; S<top_k; S++){
      for(int R = S; R<top_k; R++){
	int sid = most_common_colors[S][0];
	int rid = most_common_colors[R][0];
	
	MCN.find_L_color_trust_SR(sid,rid);
	Scol = MCN.get_S_color();
	ofile << sid << "\t" << rid << "\t" << Scol << "\t" << most_common_colors[S][1] << "\t" << most_common_colors[R][1] << "\n";
	ofile.flush();
      }
    }
    ofile.close();
    return 0;



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
    

    
    /*WRITE OUTPUT */
    /*
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
    */
    return 0;
}
