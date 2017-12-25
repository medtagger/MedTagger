#!/usr/bin/env bash

echo "Installing all APT packages..."
apt install -y make
if [ ! -e /usr/bin/python3.6 ]
then
    add-apt-repository ppa:jonathonf/python-3.6
    apt-get update
    apt install -y python3.6
    apt install -y python3.6-dev
    apt install -y python3-pip
fi

enable_hdfs=false  # HDFS is now disabled. Enable it once we will support HDFS!
if [ ! -e /opt/conda/ && enable_hdfs ]
then
    # Install Miniconda
    echo "Installing MiniConda..."
    echo "WARN: This is a workaround for problems with installing library that handles connection to the HDFS..."
    apt install -y -q curl bzip2
    curl https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -o /tmp/miniconda.sh
    /bin/bash /tmp/miniconda.sh -b -p /opt/conda
    rm /tmp/miniconda.sh
    export PATH=/opt/conda/bin:$PATH

    # Install libraries with Conda and attache them to the Linux Kernel
    conda install -y -q libhdfs3 -c conda-forge
    echo "export LD_LIBRARY_PATH=\"/opt/conda/lib:$LD_LIBRARY_PATH\"" >> /etc/environment

    # WA for errors with installing Docker after Conda
    cp -p /lib/x86_64-linux-gnu/libreadline.so.6 /opt/conda/lib/libreadline.so.6
fi

echo "Applying environment variables..."
cd /vagrant/backend
. ./devenv.sh

if [ ! -e /usr/local/bin/docker-compose ]
then
    echo "Installing Docker Compose..."
    curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

echo "Running all Docker dependencies..."
docker-compose -f /vagrant/docker-compose.yml up -d hbase postgres rabbitmq

echo "Installing all Python packages..."
make install_packages
make install_dev_packages

echo "Preparing backend..."
./scripts/dev__prepare_backend.sh
