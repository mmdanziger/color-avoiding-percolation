cmake_minimum_required(VERSION 2.6)
project(manycolornet)

add_library(manycolorlib STATIC manycolornet.cpp)

add_executable(manycolornet main.cpp)
add_executable(ascolornet main_as.cpp)
add_executable(ascolorperc main_as_perc.cpp)
add_executable(heterogenet main_hetero.cpp)
target_link_libraries(manycolornet manycolorlib)
target_link_libraries(ascolornet manycolorlib)
target_link_libraries(heterogenet manycolorlib)
target_link_libraries(ascolorperc manycolorlib)


set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Ofast -fopenmp -march=native -Wall -Wno-unused-local-typedefs")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -std=c++11 -O0 -march=native -Wall -Wno-unused-local-typedefs")

install(TARGETS manycolornet RUNTIME DESTINATION bin)
