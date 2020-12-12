/*
* Web-server setup using Simple Web Server library
* The code in this file is modified from:
* https://gitlab.com/eidheim/Simple-Web-Server/blob/master/http_examples.cpp
*
* (C) 2020 Laurens Bosman, CMPT383 Fall2020
* Released under the MIT license
* email lbosman@sfu.ca
*/

#include "client_http.hpp"
#include "server_http.hpp"
#include <future>

// Added for the json-example
#define BOOST_SPIRIT_THREADSAFE
#include <boost/property_tree/json_parser.hpp>
#include <boost/property_tree/ptree.hpp>

// needed for the index.html
#include <algorithm>
#include <boost/filesystem.hpp>
#include <fstream>
#include <vector>

#include "dataProcessing.cpp"

using namespace std;

using HttpServer = SimpleWeb::Server<SimpleWeb::HTTP>;
using HttpClient = SimpleWeb::Client<SimpleWeb::HTTP>;

// Function for activating the server
int startServer(int port) {
    HttpServer server;
    server.config.port = port;

    // Anonymous function for serving the default homepage.
    // Defaults to index.html
    // This is where you start out when calling "localhost:8080" after startup
    server.default_resource["GET"] = [](shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request) {
        try {
            auto web_root_path = boost::filesystem::canonical("web");
            auto path = boost::filesystem::canonical(web_root_path / request->path);

            // Check if path is within web_root_path
            if(distance(web_root_path.begin(), web_root_path.end()) > distance(path.begin(), path.end()) ||
                 !equal(web_root_path.begin(), web_root_path.end(), path.begin()))
                throw invalid_argument("path must be within root path");
            if(boost::filesystem::is_directory(path))
                path /= "index.html";

            SimpleWeb::CaseInsensitiveMultimap header;

            auto ifs = make_shared<ifstream>();
            ifs->open(path.string(), ifstream::in | ios::binary | ios::ate);

            if(*ifs) {
                auto length = ifs->tellg();
                ifs->seekg(0, ios::beg);

                header.emplace("Content-Length", to_string(length));
                response->write(header);

                // Trick to define a recursive function within this scope (for example purposes)
                class FileServer {
                    public:
                    static void read_and_send(const shared_ptr<HttpServer::Response> &response, const shared_ptr<ifstream> &ifs) {
                        // Read and send 128 KB at a time
                        static vector<char> buffer(131072); // Safe when server is running on one thread
                        streamsize read_length;
                        if((read_length = ifs->read(&buffer[0], static_cast<streamsize>(buffer.size())).gcount()) > 0) {
                            response->write(&buffer[0], read_length);
                            if(read_length == static_cast<streamsize>(buffer.size())) {
                                response->send([response, ifs](const SimpleWeb::error_code &ec) {
                                    if(!ec)
                                        read_and_send(response, ifs);
                                    else
                                        cerr << "Connection interrupted" << endl;
                                });
                            }
                        }
                    }
                };
            FileServer::read_and_send(response, ifs);
            }
        else
            throw invalid_argument("could not read file");
        }
        catch(const exception &e) {
            response->write(SimpleWeb::StatusCode::client_error_bad_request, "Could not open path " + request->path + ": " + e.what());
        }
    };

    //main POST code, receives data from the js query
    //returns positive or negative result to the frontend
    server.resource["^/json$"]["POST"] = [](shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request) {
        try {
            boost::property_tree::ptree pt;
            read_json(request->content, pt);

            auto data = pt.get<string>("name");
            auto dataType = pt.get<string>("dataType");

            cout << "Data: " << data << endl;

            DataProcessor processor = DataProcessor(data, dataType);
            processor.storeData();
            data = processor.calcSentiment();

            cout << "Result: " << data << endl;

            *response << "HTTP/1.1 200 OK\r\n"
                << "Content-Length: " << data.length() << "\r\n\r\n"
                << data;
        }
        catch(const exception &e) {
            *response << "HTTP/1.1 400 Bad Request\r\nContent-Length: " << strlen(e.what()) << "\r\n\r\n"
                << e.what();
        }
    };

    // POST code for receiving corrections from the frontend if a user submits it
    server.resource["^/sent$"]["POST"] = [](shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request) {
        try {
            boost::property_tree::ptree pt;
            read_json(request->content, pt);

            auto data = pt.get<string>("data");
            auto dType = pt.get<string>("dataType");
            auto sent = pt.get<string>("sentiment");

            cout << endl << "Correction" << endl;
            cout << "Data: " << data << endl;
            cout << "Data type: " << dType << endl;
            cout << "Supposed to be: " << sent << endl << endl;

            DataProcessor processor = DataProcessor(data, dType, sent);
            processor.storeCorrection();

            processor.updateModel();

            *response << "HTTP/1.1 200 OK\r\n";
        }
        catch(const exception &e) {
            *response << "HTTP/1.1 400 Bad Request\r\nContent-Length: " << strlen(e.what()) << "\r\n\r\n"
                << e.what();
        }
    };

    // Start server and receive assigned port when server is listening for requests
    promise<unsigned short> server_port;
    thread server_thread([&server, &server_port]() {
        // Start server
        server.start([&server_port](unsigned short port) {
            server_port.set_value(port);
        });
    });
    cout << "Server listening on port " << server_port.get_future().get() << endl
         << endl;

    server_thread.join();

    return 0;
}