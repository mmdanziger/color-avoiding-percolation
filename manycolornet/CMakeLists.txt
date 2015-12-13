cmake_minimum_required(VERSION 2.6)
project(manycolornet)

add_executable(manycolornet main.cpp)
add_executable(ascolornet main_as.cpp)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Ofast -fopenmp -march=native -Wall -Wno-unused-local-typedefs")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -std=c++11 -O0 -march=native -Wall -Wno-unused-local-typedefs")

install(TARGETS manycolornet RUNTIME DESTINATION bin)
