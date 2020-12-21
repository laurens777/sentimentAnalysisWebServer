# CMPT383 - Final Project

This repository contains the code to run the final project for CMPT383.
This project is a sentiment analysis model that runs on a c++ webserver. On the front-end the user can input either a tweet or a movie review and select the appropriate model. This model is a Naive Bayes classification model trained on either the NLTK Twitter corpus or the NLTK movie review corpus. This model will analyze the input and classify it as either having positive or negative sentiment.

### Languages

For this project a simple web server is created using C++ and the [Simple-Web-Server](https://gitlab.com/eidheim/Simple-Web-Server) library.  This webserver serves the main page to the user at `localhost:8080` and it will listen on port 8080 for incoming requests. Requests are made from the front-end using JavaScript REST API calls. The code responsible for implementing the sentiment analysis model is programmed in Python3 using the NLTK library.

### Inter-Language Communication Methods

The inter-language communication between the C++ server and the JavaScript front-end is done using REST API calls. At the front end JavaScript is responsible for pulling the data from the submission form and submitting a POST request using a fetch method. The C++ webserver processes these request by calling the .py files using `system()` calls. Originally the plan was to use a foreign function interface for this as can be seen by the commented out code that still remains in DataProcessor class however I was not able to get this code running on docker. 

### Deployment
Deployment is straightforward. As the only thing that should happen is to clone the code from Gitlab and run `docker-compose build $$ docker-compose up`. However there were problems with the `.gitmodules` file at one point. If CMAKE complains that there are no CMAKE files in the Simple-Web-Server folder then simply run the following commands to rectify this: `git rm -r Simple-Web-Server && git clone https://gitlab.com/eidheim/Simple-Web-Server.git` 

### Features to look for

My main struggles were with getting the webserver up and running given that I am a Linguistics student and have no experience with webservers. Because of this the webserver functionality is very limited and the JavaScript that I implemented consists of only 2 API calls. The C++ code in the `server.cpp` file is also very minimal and was adapted from https://gitlab.com/eidheim/Simple-Web-Server/blob/master/http_examples.cpp. The important features are what was written in Python. I implemented a sentiment analysis model using a Naive Bayes classifier from the NLTK library. This model was trained using corpus data provided by the NLTK library.  My references for this part are the NLTK documentation as well as the "Natural Language Processing with Python" book by Bird, Klein, and Loper.
