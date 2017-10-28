#!/usr/bin/env bash

# That's needed for Python to understand where is the root directory for parsing
export PYTHONPATH=`pwd`

# Enable virtualenv if exists
if [ -e venv ]
then
    echo "Using virtualenv from ./venv."
    . venv/bin/activate
else
    echo "Could not find any virtualenv. Skipping..."
fi
