## Running colornet ##

Requires several boost libraries, best to install all of them.  Also requires c++11 so gcc > 4.4 or so.

Recommended build from this directory:

    mkdir build
    cmake ..
    make

If you don't have cmake installed and don't want to/can't install it

    g++ -std=c++11 -march=native -O3 ../main.cpp -o colornet -lboost_program_options


run the resulting binary with flag --help to see the command line options


