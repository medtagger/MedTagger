#!/usr/bin/env bash

add-apt-repository ppa:jonathonf/python-3.6
apt update
apt install -y make
apt install -y python3.6
apt install -y python3.6-dev
apt install -y python3-pip

apt install -y postgresql-9.5
sudo -u postgres createdb dev_db
sudo -u postgres psql -c "CREATE USER dev WITH PASSWORD 'asdasd'"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE dev_db to dev"

if [ -ne /opt/conda/ ]
then
    # Install Miniconda
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

cd /vagrant
make install_packages
