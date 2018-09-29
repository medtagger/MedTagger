#!/usr/bin/env bash

# That's needed for Python to understand where is the root directory for parsing
export PYTHONPATH=`pwd`

if [ -e venv ]
then
    echo "Using virtualenv from ./venv."
    . venv/bin/activate
else
    echo "Could not find any virtualenv. Using `which python3.7` instead."
fi

echo "Applying default development configuration entries..."
. ./scripts/dev__configuration.sh

