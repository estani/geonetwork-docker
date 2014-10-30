#!/bin/bash

#nothing fancy in here, just plain old build
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
docker build -t "$(basename $SCRIPT_DIR)" "$SCRIPT_DIR"
