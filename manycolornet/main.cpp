#include <iostream>
#include <fstream>
#include <vector>
#include "manycolornet.h"


using std::vector;





int main(int argc, char **argv) {
    std::cout << "Hello, world!" << std::endl;
    uint N = argc > 1 ? atoi(argv[1]) : 100000;
    uint C = argc > 2 ? atoi(argv[2]) : 10;
    ManyColorNet MCN(N,C);
    vector<double> k_to_sample;
    uint steps=20;
    double min_power = -5;
    double max_power = 0;
    double k_crit = C/ (C - 1.f);
    double delta_power = (max_power - min_power) / (steps -1);
    k_to_sample.push_back(k_crit);
    for(uint i=0;i<steps;++i){
	k_to_sample.push_back(k_crit + pow10(min_power + i*delta_power));
    }
    for(auto to_k : k_to_sample){
	MCN.build_network_to_k(to_k);
	MCN.find_L_color();
    }
    std::ofstream ofile("/tmp/Scolor.json");
    MCN.writeHistory(ofile);
    ofile.close();
    return 0;
}
