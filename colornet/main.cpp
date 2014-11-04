#include <iostream>
#include <fstream>
#include <chrono>
#include <unistd.h>
#include <string>
#include <boost/program_options.hpp>
#include "colornet.hpp"
namespace po = boost::program_options;
using std::cout;
using std::cerr;
using std::string;

int main(int argc, char **argv) {
    srand(static_cast<unsigned>(getpid()) * std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count());
    unsigned nColors=3;
    unsigned N = 20;
    int steps;
    double fromK=0.1;
    double kRange=0.1;
    double toK=4;
    double deltaK=0.1;
    int profile=1;
    string config_file,output_file;

    try {

        po::options_description desc("Supported options",1024);
        desc.add_options()
        ("help", "produce help message")
        ("N,N",po::value<unsigned>(&N)->default_value(100), "N")
        ("Nc,c",po::value<unsigned>(&nColors)->default_value(3), "number of colors")
        ("k0",po::value<double>(&fromK)->default_value(-1), "average degree which network will be constructed from, if none supplied, defaults to k_c = N_c/(N_c-1)")
        ("k,k",po::value<double>(&toK)->default_value(5), "average degree which network will be constructed until.")
        ("krange",po::value<double>(&kRange)->default_value(-1), "extent of range of average degrees to sample past k0. If supplied, takes precedence over arg k")
        ("deltak,d",po::value<double>(&deltaK)->default_value(-1), "Calculate S_color every deltak links (1 is unnecesarily detailed), if not supplied, logspaced")
        ("steps,s",po::value<int>(&steps)->default_value(100), "Number of steps to sample.  Currently only implemented in conjunction with logspacing")
        ("profile",po::value<int>(&profile)->default_value(1), "generate profiling information overhead should be small")
        ("output,o",po::value<string>(&output_file)->default_value("Color.json"), "output file name (will be in JSON format)")
        ("config",po::value<string>(&config_file)->default_value("color.cfg"), "config file name (options overrided by command line)");
            
        po::variables_map vm;
        po::store(po::parse_command_line(argc, argv, desc), vm);
        po::notify(vm);
        std::ifstream ifs(config_file.c_str());
        if (ifs){
            cout<<"Config file read ("<<config_file<<").\n";
            po::store(po::parse_config_file(ifs,desc),vm);
            po::notify(vm);
        }

        if ((vm.count("help"))){
            cout << desc << "\n";
            return 1;
        }      
    }catch(std::exception& e) {
        cerr << "error: " << e.what() << "\n";
        return 1;
    }
        catch(...) {
        cerr << "Exception of unknown type!\n";
        return 1;
    }

    ColorNet cn(N,nColors);
    cn.profileOn(profile>0);
    cn.setLinkMeasurementResolution(deltaK);

    //This will set directly if >0 else calculate automatically
    cn.setFromK(fromK);
    if(kRange > 0)
        cn.setToKByRange(kRange);
    else
        cn.setToK(toK);
    cn.setLinkMeasurementStepCount(steps);
    cn.incrementalComponents();
    cn.setFileName(output_file);
    cn.writeResults();
    return 0;
}
