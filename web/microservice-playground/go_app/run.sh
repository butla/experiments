#!/bin/bash

root_dir=$(dirname $0)
executable=${root_dir}/app

if [ ! -a ${executable} ]; then
    go build -o ${executable} ${root_dir}/app.go
fi

GOMAXPROCS=1 ${executable}

