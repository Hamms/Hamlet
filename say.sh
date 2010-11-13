#!/bin/bash
osascript -e "set volume $1" > /dev/null
say -f $2 -v $3
