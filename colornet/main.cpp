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
    double fromK=0.1;
    double toK=4;
    int profile=1;
    string config_file,output_file;

    try {

        po::options_description desc("Supported options",1024);
        desc.add_options()
        ("help", "produce help message")
        ("N,N",po::value<unsigned>(&N)->default_value(100), "N")
        ("Nc,c",po::value<unsigned>(&nColors)->default_value(3), "number of colors")
        ("k,k",po::value<double>(&toK)->default_value(5), "average degree which network will be constructed until")
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
    cn.incrementalComponents(fromK,toK,0);
    cn.setFileName(output_file);
    cn.writeResults();
    return 0;
}
