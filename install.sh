#!/bin/bash
## This script copy the file "findall.py" to the directory bin/ on your HOME dir
## and create a symbolic link called findall
## so that you can use it from any directory like this : `findall [dir] "KetWord"`
## if ~/bin/ do not exists it will be created

if [ ! -d $HOME/bin/ ] 
then
    mkdir $HOME/bin/
fi

cp findall.py $HOME/bin/.
ln -s $HOME/bin/findall.py $HOME/bin/findall

## Massy Kezzoul
## github -> https://github.com/massykezzoul/find-inside
