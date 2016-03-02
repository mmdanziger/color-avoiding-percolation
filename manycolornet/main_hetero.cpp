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
	for(double k=1; k<=7; k+=dk)
	    k_to_sample.push_back(k);
	for(auto to_k : k_to_sample){
	  MCN.build_network_to_k(to_k);
	  MCN.find_L_color_ST();
	}
	std::ofstream ofile("/tmp/S_color1.json");
	MCN.writeColorHistory(ofile);
	ofile.close();
	return 0; 
      }
      case 2: {
	double r3=0.2;
	double dr=0.01;
	vector<int> S_set{0,1};
	MCN.set_S_set(S_set);
	vector<int> T_set{0,1};
	MCN.set_T_set(T_set);
	C = 3;
	MCN.build_network_to_k(4);
	vector<pair<double,uint>> history;
	for(double r1=0.4;r1<=0.8;r1+=dr){
	  vector<double> rates{r1,1 - r3 - r1,r3};
	  MCN.initialize_heterogeneous_colors(rates);
	  MCN.find_L_color_ST();
	  history.push_back(std::make_pair(r1,MCN.get_S_color()));
	}
	std::ofstream ofile("/tmp/S_color2.json");
	jsonPairArray(history,ofile);
	return 0;
      }
      case 3: {
	C=3;
	vector<int> S_set{0,1};
	MCN.set_S_set(S_set);
	vector<int> T_set{0,1};
	MCN.set_T_set(T_set);
	uint steps=20;
	double min_power = -5;
	double max_power = 1;
	double delta_power = (max_power - min_power) / (steps -1);
	k_crit = 1.25;
	k_to_sample.push_back(k_crit);
	for(uint i=0;i<steps;++i){
	    k_to_sample.push_back(k_crit + pow10(min_power + i*delta_power));
	}
	double r1 = 0.2;
	map<std::string,std::vector<uint>> history;

	double r2=0.2;
	vector<double> rates{r1,r2,1 - r1 - r2};
	MCN.initialize_heterogeneous_colors(rates);

	for(auto to_k :  k_to_sample){
	  MCN.build_network_to_k(to_k);
	  MCN.find_L_color_ST();
	  history["r2 = 0.2"].push_back(MCN.get_S_color());
	}
	MCN.clear_network();
	
	r2=0.17;
	rates[1] = r2;
	rates[2] = 1 - r2 - r1;
	MCN.initialize_heterogeneous_colors(rates);
	for(auto to_k :  k_to_sample){
	  MCN.build_network_to_k(to_k);
	  MCN.find_L_color_ST();
	  history["r2 = 0.17"].push_back(MCN.get_S_color());
	}
	MCN.clear_network();
	
	r2=0.1;
	rates[1] = r2;
	rates[2] = 1 - r2 - r1;
	MCN.initialize_heterogeneous_colors(rates);
	for(auto to_k :  k_to_sample){
	  MCN.build_network_to_k(to_k);
	  MCN.find_L_color_ST();  
	  history["r2 = 0.1"].push_back(MCN.get_S_color());
	}
	std::ofstream kofile("/tmp/k_for_3.json");
	jsonArray(k_to_sample,kofile);
	std::ofstream ofile("/tmp/S_color3.json");
	jsonMapOfArrays(history,ofile);
	return 0;
      }
      default:
	std::cerr<<"Pick an example number between 1 and 4!\n";
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

    return 0;
}

