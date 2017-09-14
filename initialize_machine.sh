#!/usr/bin/env bash

add-apt-repository ppa:jonathonf/python-3.6
apt update
apt install -y make
apt install -y python3.6
apt install -y python3-pip

apt install -y postgresql-9.5
sudo -u postgres createdb dev_db
sudo -u postgres psql -c "CREATE USER dev WITH PASSWORD 'asdasd'"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE dev_db to dev"

cd /vagrant
make install_packages
