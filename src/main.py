from os import getenv
from paramiko import AutoAddPolicy, SSHClient
from datetime import date
from dotenv import load_dotenv
import time
import paramiko

path = ''

def main():  
    ssh_connection = establish_connection_using_jumphost('14.14.14.28', 'cisco', 'cisco')
    execute_command(ssh_connection, 'term len 0')
    save_output(ssh_connection, 'sh ip int brief')
    pass


class UnconfiguredEnvironment(Exception):
    '''Exception class for unconfigured environment variables'''
    pass


def load_environment_variables() -> dict[str, str]:
    '''
    method used to load environment variables
    '''
    environment_variables_list = ['JUMPHOST_IP', 'JUMPHOST_PORT', 'JUMPHOST_USER', 'JUMPHOST_PASS']
    vars = dict()
    for var in environment_variables_list:
        if not (env_val := getenv(var, None)):
            raise UnconfiguredEnvironment(f"{var} is not configured")
        vars[var] = env_val
    return vars


def establish_connection_using_jumphost(target:str, tuser:str, tkey:str, port=22) -> SSHClient:
    '''
    method used to connect to a target, using a jumphost inbetween
    '''
    jumphost_ssh_connection = establish_connection_to_jumphost(True)
    time.sleep(.5)
    jumphost_ssh_connection.send('ssh -l '+tuser+' -p '+str(port)+' '+target+'\n')
    jumphost_ssh_connection.recv(65535)
    time.sleep(2)
    jumphost_ssh_connection.send(tkey+'\n')
    jumphost_ssh_connection.recv(65535)
    time.sleep(.5)
    return jumphost_ssh_connection


def establish_connection_to_jumphost(mute=False) -> SSHClient:
    '''
    method used to establish a connection to the jumphost
    '''
    load_dotenv()
    try:
        vars = load_environment_variables()
    except UnconfiguredEnvironment as e:
        exit(e)
    ssh_connection = establish_connection(vars['JUMPHOST_IP'], vars['JUMPHOST_USER'], vars['JUMPHOST_PASS'], vars['JUMPHOST_PORT'], mute)
    return ssh_connection


def establish_connection(host:str, user:str, key:str, port=22, mute=False) -> SSHClient:
    '''
    method used to establish a connection using the address, port, username and password
    return a established connection
    '''
    ssh_connection_pre = SSHClient()
    ssh_connection_pre.set_missing_host_key_policy(AutoAddPolicy())
    ssh_connection_pre.connect(hostname=host, port=port, username=user, password=key)
    ssh_connection = ssh_connection_pre.invoke_shell()
    output = ssh_connection.recv(65535)
    if not mute:
        print(output.decode("utf-8"))
    return ssh_connection


def execute_command(ssh_connection:SSHClient, command:str, readsize=65535) -> str:
    '''
    method used to execute a command using a established connection, prints the output from the command
    '''
    ssh_connection.send(command+'\n')
    time.sleep(10)
    return ssh_connection.recv(readsize).decode("utf-8")
    


def close_connection(ssh_connection:SSHClient) -> None:
    '''
    method used to close a connection
    '''
    ssh_connection.close()


def save_output(ssh_connection:SSHClient, command:str, readsize=65535) -> None:
    '''
    method used to execute a command and save its output to a file, following the naming format "hostname-YYYY-MM-DD.txt" for the output file
    '''
    response = execute_command(ssh_connection, command, readsize)
    hostname = response.split('\n')[-1][:-1]+'-'+str(date.today())+'.txt'
    file = open(path+hostname, 'w')
    file.write(response)
    file.close()


if __name__=="__main__":
    main()
