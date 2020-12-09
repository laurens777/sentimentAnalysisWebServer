/* ----------------------------------------------------------------
* Main program entry for CMPT383 final project
*
* (C) 2020 Laurens Bosman, CMPT383 Fall2020
* Released under the MIT license
* email lbosman@sfu.ca
* ----------------------------------------------------------------
*/

#include "server.cpp"

using namespace std;

int checkArguments(int, char[]);


int main(int argc, char *argv[]) {
    //if (checkArguments(argc, *argv) == 0) {
    //    return 0;
    //}

    startServer(8080);
}

int checkArguments(int argc, char argv[]) {
    if (argc != 2) {
        cerr << "Not enough arguments received!" << endl;
        return 0;
    }

    return 1;
}