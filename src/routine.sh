#!/bin/bash
#directory in which the config is stored
DIR="/home/elbrus/Desktop/ssh-manager/config"

echo "info: retrieving configurations"
#execute python job
python3 /home/elbrus/Desktop/ssh-manager/src/main.py

#set current date in the Format YYYY-MM-DD-HH:MM:SS
now=$(date +%F-%T)

if [ -d "$DIR" ]; then
    echo "info: starting with version control"
    cd $DIR

    #loop through every directory
    for f in *; do
        if [ -d "$f" ]; then
            cd $f
            echo "info: working in directory '$f'"
            
            #loop through every file in directory
            for c in *; do
                echo "info: working in file '$c'"
                add_reply=$(git add $c)
                commit_reply=$(git commit -m "$now--$f--$c")
            done
            cd ..
        fi
    done
    echo "info: everything saved!"
else
    echo "error: please run 'initialise.sh' first!"
fi