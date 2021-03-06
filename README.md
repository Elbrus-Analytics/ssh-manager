# ssh-manager
Directory for all shh + git related scripts, templates and other files
Used to connects to devices using ssh and establish a interactive bash session.
Gathers Job by connecting to a database. Executes these jobs and saves the output in a version control system.


## features

  - can ssh key depending on the given parameters
  - ssh connections using a jump server
  - ssh connections to the jump server
  - save the output of command to files
  - version control system ;)
  - automatically initialise a git repository for the outputs
  - automatically add and commit changes in the output files
  - use systemd to automate the script
  - setup script

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
  - run 'setup.sh'

install dependencies

```bash
    pip3 install -r requirements.txt
```

#### Option 1: automatic execution of the script

##### deployment
  - change path of the working directory in 'ssh-manager.service.example'
  - change the user in 'ssh-manager.service.example'
  - in 'ssh-manager-schedule.timer.example' set custom times if wanted

copy the service script

```bash
    cp src/ssh-manager.service.example /etc/systemd/system/ssh-manager.service
```

copy the scheduler

```bash
    cp src/ssh-manager-schedule.timer.example /etc/systemd/system/ssh-manager-schedule.timer
```

reload systemctl daemon

```bash
    systemctl daemon-reload
```

enable the service

```bash
    systemctl enable ssh-manager.service
```
-> should create a output like 

```bash
    Created symlink /etc/systemd/system/multi-user.target.wants/ssh-manager.service → /etc/systemd/system/ssh-manager.service.
```

enable the timer

```bash
    systemctl enable ssh-manager-schedule.timer
```

start the timer

```bash
    systemctl start ssh-manager-schedule.timer
```

check if timer is running

```bash
    systemctl status ssh-manager-schedule.timer
```

##### routine.sh script should now be automaticaly executed in the interval which is declaired in 'ssh-manger-schedule.timer'  

#### Option 2: manual execution of the script

run routine script

```bash
    src/routine.sh
```

## hint
use 'term len 0' on cisco cli to show configuration without breaks
