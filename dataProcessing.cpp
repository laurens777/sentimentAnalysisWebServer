#include <string>
#include <iostream>
#include <fstream>

using namespace std;

class DataProcessor {
    public:
    string data;
    string fileName;

    DataProcessor(string content) {
        data = content;
    }

    void calcSentiment() {
        string command = "python3 ../python/main.py " + fileName;

        cout << command << endl;
        system(command.c_str()); 

        return;
    }

    void storeData() {
        ofstream fileWriter;
        fileWriter.open("tempData.txt");
        fileWriter << data;
        fileWriter.close();

        fileName = "tempdData.txt";

        return;
    }
};