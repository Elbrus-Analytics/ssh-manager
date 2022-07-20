#!/bin/bash
#script to create a folder where config files are stored, also initialises a git repo in the config folder

source ../.env

#directory in which the config is stored
DIR=$CONFIGPATH

if [ -d "$DIR" ]; then
    echo "error: config folder already exists!"
else
    #creating folder
    mkdir $DIR
    cd $DIR

    #initialising git
    git init
    git config --global user.name "ssh-script"
    git config --global user.email "ssh-script@elbrus-analytics.at"
    echo "info: created config folder!"
fi