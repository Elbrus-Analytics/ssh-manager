# ssh -  git
Directory for all shh + git related scripts, templates and other files
Used to connects to devices using ssh and establish a interactive bash session.

## features
possibility to: - connect using a jump host
                - save the output a file

## dependencies
see in 'requirements.txt'

## usage
uses .env variables to connect to the jumphost
run from inside '/src' directory

## hint
use 'term len 0' on cisco cli to show configuration without breaks

## deployment
add a '.env' file corresponding to '.env.example'
check the operating system of the jump host -> change ssh connection command in 'establish_connection_using_jumphost' in 'main.py'
change 'directory' variable in 'main.py'
change 'DIR' variable in 'initialise.sh'
change 'DIR' variable in 'routine.sh'
change path to python script in 'routine.sh'

## run locally

clone the project

```bash
    git clone https://github.com/Elbrus-Analytics/ssh-manager.git
```

follow the deployment guide

go to project directory

```bash
    cd ssh-manager
```

install dependencies

```bash
    pip install -r requirements.txt
```

run initialise script

```bash
    src/initialise.sh
```

run routine script

```bash
    src/routine.sh
```