FROM debian:12

USER root
WORKDIR /root

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_ROOT_USER_ACTION=ignore

RUN apt-get update -y
RUN apt-get upgrade -y

# Install Python and dependencies
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --break-system-packages 

# Generate ssb lineorder table
RUN apt-get install -y git
RUN git clone https://github.com/vadimtk/ssb-dbgen.git
WORKDIR /root/ssb-dbgen
RUN make
RUN ./dbgen -s 0.1 -T l
RUN cp lineorder.tbl ../lineorder.csv

WORKDIR /root
RUN apt-get install -y vim \
    net-tools
