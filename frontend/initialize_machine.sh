#!/usr/bin/env bash

echo "Install NodeJS"
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
apt-get update
apt install -y nodejs

echo "Download dependencies"
cd /vagrant/frontend/
npm install -g npm-install-retry
npm-install-retry -- --no-bin-links
