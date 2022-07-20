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

read -p "Where do you want the config to be stored: (absolut path) " path
read -p "Where is the 'main.py' file stored: (absolut path) " pathtomain
while true; do
echo 
echo "Do you want to store the config files at \"$path\"?" 
read -p "Is your 'main.py' stored at \"$pathtomain\"? (y/n/exit) " confirm
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

# change Path for '.env'
sed "21 c\
CONFIGPATH=\"$path\"" ../.env > tmp.env
cat tmp.env > ../.env
rm -rf tmp.env

sed "22 c\
MAINPATH=\"$pathtomain\"" ../.env > tmp.env
cat tmp.env > ../.env
rm -rf tmp.env

echo
echo "The paths have been set!"
echo

read -p "Do you want to configure the systemd Service? (y/n/exit) " confirm
case $confirm in
    [yY] | "yes" | "Yes" ) echo 
        read -p "Which User should execute the Service? " user
    # change Path in ssh-manager.service.example
        sed "10 c\
        WorkingDirectory=$scriptpath" ssh-manager.service.example > tmp.ssh-manager.service.example
        cat tmp.ssh-manager.service.example > ssh-manager.service.example
        rm -rf tmp.ssh-manager.service.example
    # change User in ssh-manager.service.example
        sed "8 c\
        User=$user" ssh-manager.service.example > tmp.ssh-manager.service.example
        cat tmp.ssh-manager.service.example > ssh-manager.service.example
        rm -rf tmp.ssh-manager.service.example

        clear
        echo "The systemd Service has been configured!"
        echo
        ;;
    [nN] | "no" | "No" ) clear 
        echo proceeding without configuring systemd Service
        echo
        ;;
    [eE] | "exit" | "Exit" ) echo exiting...;
            exit;;
    * ) echo invalid response;;
esac


read -p "Do you want to run the initialise script? (y/n/exit) " confirm
case $confirm in
    [yY] | "yes" | "Yes" ) ./initialise.sh;;
    [nN] | "no" | "No" ) clear
     echo proceeding without running initialise.sh
                        ;;
    [eE] | "exit" | "Exit" ) echo exiting...;
            exit;;
    * ) echo invalid response;;
esac

echo 
echo "finished setup"