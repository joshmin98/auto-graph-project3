#!/usr/bin/env bash

if [ -z $1 ]; then
    echo "\n./run.sh TARGET_FILE OUTPUT_FILE\n"
    exit 1
fi
if [ -z $2 ]; then
    echo "\n./run.sh TARGET_FILE OUTPUT_FILE\n"
    exit 1
fi

if test -f "./run.lock"; then
    pipenv run python graphify.py $1 $2
else
    pipenv install
    touch ./run.lock
    pipenv run python graphify.py $1 $2
fi
