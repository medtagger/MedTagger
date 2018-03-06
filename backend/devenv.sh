#!/usr/bin/env bash

# That's needed for Python to understand where is the root directory for parsing
export PYTHONPATH=`pwd`
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/usr/lib64:/usr/lib:/lib

if [ -e venv ]
then
    echo "Using virtualenv from ./venv."
    . venv/bin/activate
else
    echo "Could not find any virtualenv. Using `which python3.6` instead."
fi

echo "Applying default development configuration entries..."
. ./scripts/dev__configuration.sh

