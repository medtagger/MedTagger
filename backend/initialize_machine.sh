#!/usr/bin/env bash

echo "Installing all APT packages..."
sudo apt-get install -y make
if [ ! -e /usr/bin/python3.7 ]
then
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install -y python3.7
    sudo apt-get install -y python3.7-dev
    sudo apt-get install -y python3-pip
fi

echo "Applying environment variables..."
cd /vagrant/backend
. ./devenv.sh

if [ ! -e /usr/local/bin/docker-compose ]
then
    echo "Installing Docker Compose..."
    sudo curl -L https://github.com/docker/compose/releases/download/1.24.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

echo "Running all Docker dependencies..."
docker-compose -f /vagrant/docker-compose.yml up -d cassandra postgres rabbitmq

echo "Installing all Python packages..."
make install_packages
make install_dev_packages

echo "Preparing backend..."
./scripts/dev__prepare_backend.sh

