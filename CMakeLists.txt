cmake_minimum_required(VERSION 3.13)

# set the project name
project(Project)

add_subdirectory(Simple-Web-Server)

find_package(Boost COMPONENTS system thread filesystem)
find_package(Python3 REQUIRED)
find_package(PythonLibs REQUIRED)

include_directories(/usr/local/include/python3.8/)
include_directories(${PYTHON_INCLUDE_DIRS})



if(Boost_FOUND)
    add_executable(main main.cpp dataProcessing.cpp)
    target_link_libraries(main simple-web-server)
    target_link_libraries(main ${PYTHON_LIBRARIES})
    target_link_libraries(main ${Boost_LIBRARIES})
    target_include_directories(main PRIVATE ${Boost_INCLUDE_DIR})
endif()
