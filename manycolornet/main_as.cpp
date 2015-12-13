#include <iostream>
#include <fstream>
#include <vector>
#include "manycolornet.cpp"


using std::vector;





int main(int argc, char **argv) {
    srand(time(0));
    string data_dir = argc > 1 ? string(argv[1]) : "/home/micha/secret_mp/real_data/";
    ManyColorNet MCN(data_dir + "caide-latest-complete-direct-vertex-colors-only.txt",data_dir + "caide-latest-complete-direct-edge-list.txt");
    MCN.find_L_color();
    MCN.writeHistory(std::cout);
    /*WRITE OUTPUT */
    std::ofstream ofile("/tmp/AS_colors.json");
    MCN.writenodecolors(ofile);
    ofile.close();
    return 0;
}
