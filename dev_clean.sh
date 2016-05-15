#!/bin/bash

set -e
set -u

initial_check () {
    if [[ ! "$(pwd)" == *betterinformatics ]]; then
        echo "Please run this script from the root (git) directory\n"
        exit 1
    fi

    echo "This script is going to remove pages history.\n"
    echo "Are you sure you want to run it? [Y,n]"
    read -p " " -n 1 -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        echo # for newline
        exit 1
    fi

    echo # for newline
}

initial_check

rm -rv ./pages/history/*
