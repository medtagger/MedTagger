#!/usr/bin/env bash
if [ "$TRAVIS_BRANCH" == "master" ] && [ "$1" == "staging" ]; then
    echo "Create directory for staging key..."
    mkdir -p /tmp/.travis/
    echo "Decrypt private key to the staging server..."
    openssl aes-256-cbc -K $encrypted_9953cb5dbc4f_key -iv $encrypted_9953cb5dbc4f_iv -in .travis/staging.key.enc -out /tmp/.travis/staging.key -d
    echo "Enabling SSH Agent..."
    eval "$(ssh-agent -s)"
    echo "Adding private key to the staging server..."
    chmod 600 /tmp/.travis/staging.key
    ssh-add /tmp/.travis/staging.key
    echo "Executing deployment on the server..."
    ssh $SSH_DESTINATION_USER__STAGING@$SSH_DESTINATION_HOST__STAGING -p $SSH_DESTINATION_PORT__STAGING "echo Hello"
fi
