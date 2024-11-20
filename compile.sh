#!/bin/bash

install_dir=/usr/local/bin

if [ ! -d $install_dir ]; then
    mkdir -p $install_dir
fi

c_file=$(mktemp /tmp/fan_control.XXXXXX.c)

cython3 main.py --embed -o $c_file 

gcc -Os -I /usr/include/python3.11 -o $install_dir/fan_control $c_file -lpython3.11 -lpthread -lm -lutil -ldl

rm $c_file