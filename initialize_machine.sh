#!/usr/bin/env bash

apt install -y make
apt install -y python3.6
apt install -y python3.6-dev
apt install -y python3-pip

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
export PYTHONPATH=`pwd`

echo "Installing all Python packages..."
make install_packages

echo "Migrating SQL database..."
alembic upgrade head

echo "Migrating HBase database..."
python3.6 scripts/migrate_hbase.py --yes

echo "Apply database fixtures..."
python3.6 data_labeling/database/fixtures.py

echo "Populate database with default user accounts..."
python3.6 scripts/add_default_dev_accounts.py
