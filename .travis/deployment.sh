#!/usr/bin/env bash
if [ "$TRAVIS_BRANCH" == "master" ] && [ "$1" == "staging" ]; then
    eval "$(ssh-agent -s)"
    ssh-add ./.travis/staging.key
    ssh $SSH_DESTINATION_HOST__STAGING -p $SSH_DESTINATION_PORT__STAGING "echo Hello"
fi
