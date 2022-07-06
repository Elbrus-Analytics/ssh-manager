# ssh -  git
Directory for all shh + git related scripts, templates and other files
Used to connects to devices using ssh and establish a interactive bash session.
Save the output in VSC.

## features
  - ssh connections using a jump server
  - ssh connections to the jump server
  - save the output of command to files
  - automatically initialise a git repository for the outputs
  - automatically add and commit changes in the output files

## dependencies
see in 'requirements.txt'

## run locally

clone the project

```bash
    git clone https://github.com/Elbrus-Analytics/ssh-manager.git
```

go to project directory

```bash
    cd ssh-manager
```

### deployment
  - add a '.env' file corresponding to '.env.example'
  - check the operating system of the jump host -> change ssh connection command in 'establish_connection_using_jumphost' in 'main.py'
  - change 'directory' variable in 'main.py'
  - change 'DIR' variable in 'initialise.sh'
  - change 'DIR' variable in 'routine.sh'
  - change path to python script in 'routine.sh'

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

## hint
use 'term len 0' on cisco cli to show configuration without breaks
