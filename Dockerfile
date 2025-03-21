FROM ubuntu:24.10

USER root
WORKDIR /root

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_ROOT_USER_ACTION=ignore

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y \
        git \
        sudo

# Add user dev group dev
ARG USERNAME=dev
ARG USER_UID=1001
ARG USER_GID=1001

RUN groupadd --gid $USER_GID $USERNAME
RUN useradd --uid $USER_UID --gid $USER_GID --create-home $USERNAME
    
# Add the user to the sudo group without requiring a password
RUN echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $USERNAME

WORKDIR /home/$USERNAME
RUN git clone https://github.com/p4lang/open-p4studio.git

WORKDIR /home/$USERNAME/open-p4studio
RUN git submodule update --init --recursive
#RUN ./p4studio/p4studio profile apply ./p4studio/profiles/testing.yaml
