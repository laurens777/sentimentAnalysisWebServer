cmake_minimum_required(VERSION 3.10)

# set the project name
project(Project)

add_subdirectory(Simple-Web-Server)

find_package(Boost 1.53.0 COMPONENTS system thread filesystem)
if(Boost_FOUND)
    add_executable(test test.cpp)
    target_link_libraries(test simple-web-server)
    target_link_libraries(test ${Boost_LIBRARIES})
    target_include_directories(test PRIVATE ${Boost_INCLUDE_DIR})
endif()
