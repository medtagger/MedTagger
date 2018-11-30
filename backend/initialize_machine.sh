#!/usr/bin/env bash

echo "Installing all APT packages..."
apt install -y make
if [ ! -e /usr/bin/python3.7 ]
then
    add-apt-repository ppa:deadsnakes/ppa
    apt-get update
    apt-get install -y python3.7
    apt-get install -y python3.7-dev
    apt-get install -y python3-pip
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
docker-compose -f /vagrant/docker-compose.yml up -d cassandra postgres rabbitmq

echo "Installing all Python packages..."
make install_packages
make install_dev_packages

echo "Preparing backend..."
./scripts/dev__prepare_backend.sh

