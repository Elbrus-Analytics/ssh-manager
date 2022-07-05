DIR="../config"
if [ -d "$DIR" ]; then
    echo "config folder already exists!"
else
    mkdir $DIR
    cd $DIR
    git init
    git config --global user.name "ssh-script"
    git config --global user.email "ssh-script@elbrus-analytics.at"
    echo "info: created config folder!"
fi