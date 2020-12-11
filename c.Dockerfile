FROM debian:10
FROM python:3.8

RUN apt-get update \
  && apt-get install -y build-essential gcc g++ clang cmake libssl-dev libboost-filesystem-dev libboost-thread-dev\
  && apt-get clean python3-setuptools python3-dev python3\
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install nltk

RUN python -m nltk.downloader twitter_samples
RUN python -m nltk.downloader stopwords

WORKDIR /project
COPY . .

#RUN gcc -Wall -o hello hello-world/hello.c
#RUN clang -Wall -o hello hello-world/hello.c
#RUN g++ -Wall -o hello hello-world/hello.cpp
#RUN clang++ -Wall -o hello hello-world/hello.cpp
RUN cmake -H. -Bbuild && cmake --build build

CMD ./build/main 8080