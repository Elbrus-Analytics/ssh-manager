#!/usr/bin/env bash
echo "Setup for ssh-manager"
while true; do
read -p "Do you want to proceed? (y/n) " yn
case $yn in
    [yY] | "yes" | "Yes" ) echo we will proceed;
            break;;
    [nN] | "no" | "No" ) echo exiting...;
            exit;;
    * ) echo invalid response;;
esac
done
echo
sleep 0.25

read -p "Where do you want the config to be stored: " path

while true; do
echo 
read -p "Do you want to store the config files at \"$path\"? (y/n/exit) " confirm
case $confirm in
    [yY] | "yes" | "Yes" ) echo we will proceed;
            break;;
    [nN] | "no" | "No" ) clear;
            read -p "Where do you want the config to be stored: " path;;
    [eE] | "exit" | "Exit" ) echo exiting...;
            exit;;
    * ) echo invalid response;;
esac
done
clear

script=$(readlink -f $0)
scriptpath=`dirname $script`

# change Path for routine.sh
sed "6 c\
DIR=\"$path\"" routine.sh > tmp.routine.txt
cat tmp.routine.txt > routine.sh
rm -rf tmp.routine.txt

sed "10 c\
python3 $scriptpath/main.py" routine.sh > tmp.routine.txt
cat tmp.routine.txt > routine.sh
rm -rf tmp.routine.txt

# change Path for initialise.sh
sed "5 c\
DIR=\"$path\"" initialise.sh > tmp.initialise.txt
cat tmp.initialise.txt > initialise.sh
rm -rf tmp.initialise.txt

# change Path for main.py
sed "14 c\
directory = '$path'" main.py > tmp.main.py
cat tmp.main.py > main.py
rm -rf tmp.main.py

# change Path in ssh-manager.service.example
sed "10 c\
WorkingDirectory=$scriptpath" ssh-manager.service.example > tmp.ssh-manager.service.example
cat tmp.ssh-manager.service.example > ssh-manager.service.example
rm -rf tmp.ssh-manager.service.example


echo
echo "The path has been set to \"$path\"!"
echo


read -p "Do you want to run the initialise script? (y/n/exit) " confirm
case $confirm in
    [yY] | "yes" | "Yes" ) ./initialise.sh;;
    [nN] | "no" | "No" ) echo proceeding without running initialise.sh;;
    [eE] | "exit" | "Exit" ) echo exiting...;
            exit;;
    * ) echo invalid response;;
esac

echo 
echo "finished setup:"
echo "1. $path"
echo "2. $scriptpath"