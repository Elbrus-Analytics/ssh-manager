#!/bin/bash
#script to collect data using the python job, checking for changes in config folder -> if there are some, these changes are added and commited

source ../.env

#directory in which the config is stored
DIR=$CONFIGPATH

echo "info: retrieving configurations"
#execute python job
python3 $MAINPATH

#set current date in the Format YYYY-MM-DD-HH:MM:SS
now=$(date +%F-%T)

if [ -d "$DIR" ]; then
    echo "info: starting with version control"
    cd $DIR

    #loop through every directory
    for f in *; do
        if [ -d "$f" ]; then
            echo "info: working in directory '$f'"
            cd $f
            
            #loop through every file in directory
            for c in *; do
                echo "info: working in file '$c'"

                #executing git commands
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