#include <algorithm>
#include <fstream>
#include "manycolornet.h"
#include <assert.h>
#include <cstdlib>
#include <iostream>



int main(int argc, char **argv) {
    uint N = argc > 1 ? atoi(argv[1]) : 100000;
    uint example_number = argc > 2 ? atoi(argv[2]) : 1;
    int C = 3;
    
    double k_crit = C/ (C - 1.f);
    vector<double> k_to_sample;

    ManyColorNet MCN(N,C);
    
    switch(example_number){
      case 1: {
	vector<double> rates{0.5,0.3,0.2};
	MCN.initialize_heterogeneous_colors(rates);
	vector<int> S_set{0,1};
	MCN.set_S_set(S_set);
	vector<int> T_set{0,1};
	MCN.set_T_set(T_set);
	C = rates.size();
	double rc = 0.5;
	k_crit = 1 / (1 - rc);
	double dk=0.1;
	for(double k=1; k<7; k+=dk)
	    k_to_sample.push_back(k);
	break; }
      default:
	std::cerr<<"Pick an example number!\n";
	return 1;
	
    }
    
    if(k_to_sample.empty()){
	uint steps=20;
	double min_power = -5;
	double max_power = 0;
	double delta_power = (max_power - min_power) / (steps -1);
	k_to_sample.push_back(k_crit);
	for(uint i=0;i<steps;++i){
	    k_to_sample.push_back(k_crit + pow10(min_power + i*delta_power));
	}
    }
    for(auto to_k : k_to_sample){
	MCN.build_network_to_k(to_k);
	MCN.find_L_color_ST();
    }
    std::ofstream ofile("/tmp/Scolor.json");
    MCN.writeHistory(ofile);
    ofile.close();
    return 0;
}

