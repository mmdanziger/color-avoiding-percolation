project(colornet)
cmake_minimum_required(VERSION 2.8)
find_package(Boost COMPONENTS program_options)

if(Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS})
    add_executable(colornet main.cpp)
    target_link_libraries(colornet ${Boost_LIBRARIES})                                                                                                                                                                                                                            
endif()

 set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -O3 -march=native -Wall -Wno-unused-local-typedefs")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -std=c++11 -O0 -march=native -Wall -Wno-unused-local-typedefs")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -g3 -Wall -Wno-unused-local-typedefs")

install(TARGETS colornet RUNTIME DESTINATION bin)
