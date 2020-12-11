/*
* DataProcessor class for taking care of storing data
* and calling the python scripts for doign the sentiment analysis
*
* (C) 2020 Laurens Bosman, CMPT383 Fall2020
* Released under the MIT license
* email lbosman@sfu.ca
*/

#include <string>
#include <iostream>
#include <fstream>

//#include <Python.h>

using namespace std;

class DataProcessor {
    public:
    string data;
    string dataType;
    string fileName;

    DataProcessor(string content, string dType) {
        data = content;
        dataType = dType;
    }

    //calcSentiment calls the python script and returns "Postive" or "Negative"
    string calcSentiment() {
        string cmd = "python3 ./python/main.py " + fileName + " " + dataType;
        //system(command.c_str()); 

        //wchar_t *program = Py_DecodeLocale("./", NULL);
        //if (program == NULL) {
        //    fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        //    exit(1);
        //}
        //Py_SetProgramName(program);  /* optional but recommended */
        //Py_Initialize();
        //PyObject *pName, *pModule, *pDict, *pFunc, *pArgs, *pValue;
        //pName = PyUnicode_FromString("Sample");
        //pModule = PyImport_Import(pName);
        //if (pModule == nullptr)
        //{
        //    PyErr_Print();
        //    std::exit(1);
        //}
        //pFunc = PyDict_GetItemString(pDict, "add");
        //pArgs = PyTuple_New(2);
        //pValue = PyLong_FromLong(2);
        //PyTuple_SetItem(pArgs, 0, pValue);
        //PyTuple_SetItem(pArgs, 1, pValue);
        //PyObject* pResult = PyObject_CallObject(pFunc, pArgs);
        //long result = PyLong_AsLong(pResult);
        //Py_Finalize();
        //printf("The result is %d.\n", result); 

        //since the above commented lines do not seem to work in docker
        //this is a workaround for getting my result from the python code:
        string result;
        FILE * stream;
        const int max_buffer = 256;
        char buffer[max_buffer];

        stream = popen(cmd.c_str(), "r");
        if (stream) {
            while (!feof(stream)) {
                if (fgets(buffer, max_buffer, stream) != NULL) {
                    result.append(buffer);
                }
            }
        pclose(stream);
        }

        return result;
    }

    //store data to a text file so that the Python script is able to access it
    void storeData() {
        ofstream fileWriter;
        fileWriter.open("tempData.txt");
        fileWriter << data;
        fileWriter.close();

        fileName = "tempData.txt";

        return;
    }
};