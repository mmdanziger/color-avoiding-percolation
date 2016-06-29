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
    auto out = MCN.count_same_color_links(samples);
    jsonArrayofArrays(out,std::cout);
    
    
}