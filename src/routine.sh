DIR="../config"
#python -> schreibt files
now=$(date +%F-%T)
if [ -d "$DIR" ]; then
    cd $DIR
    for f in *; do
        if [ -d "$f" ]; then
            cd $f
            echo "info: working in directory '$f'"
            for c in *; do
                echo "info: working in file '$c'"
                git add $c
                git commit -m "$now--$f--$c"
            done
            cd ..
        fi
    done
    echo "info: everything saved!"
else
    echo "info: please run 'initialise.sh' first!"
fi