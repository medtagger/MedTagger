#!/usr/bin/env bash

add-apt-repository ppa:jonathonf/python-3.6
apt update
apt install -y python3.6
apt install -y python3.6-dev
apt install -y python3-pip
apt install -y make

# Install Miniconda
apt install -y -q curl bzip2
curl https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -o /tmp/miniconda.sh
/bin/bash /tmp/miniconda.sh -b -p /opt/conda
rm /tmp/miniconda.sh
export PATH=/opt/conda/bin:$PATH

# Install libraries with Conda and attache them to the Linux Kernel
conda install -y -q libhdfs3 -c conda-forge
echo "export LD_LIBRARY_PATH=\"/opt/conda/lib:$LD_LIBRARY_PATH\"" >> /etc/environment

cd /vagrant
make install_packages
