#!/usr/bin/env bash

start-all.sh
mr-jobhistory-daemon.sh start historyserver
nohup jupyter lab >error.log &
