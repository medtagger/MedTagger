#!/usr/bin/env bash

add-apt-repository ppa:jonathonf/python-3.6
apt update
apt install -y python3.6
apt install -y make
apt install -y python3-pip

cd /vagrant
make install_packages
