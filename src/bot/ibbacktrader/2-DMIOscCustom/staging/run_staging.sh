#!/usr/bin/env bash

echo "The script you are running has basename $( basename -- "$0"; ), dirname $( dirname -- "$0"; )";
echo "The present working directory is $( pwd; )";

cd $( dirname -- "$0"; ) && mkdir -p ./log
python DMIStoch.py >> "./log/stage_log.txt"
