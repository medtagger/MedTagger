#!/usr/bin/env bash
if [ "$TRAVIS_BRANCH" == "master" ] && [ "$1" == "staging" ]; then
    echo "Enabling SSH Agent..."
    eval "$(ssh-agent -s)"
    echo "Adding private key to the staging server..."
    ssh-add /tmp/.travis/staging.key
    echo "Executing deployment on the server..."
    ssh $SSH_DESTINATION_HOST__STAGING -p $SSH_DESTINATION_PORT__STAGING "echo Hello"
fi
