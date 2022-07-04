from sys import stderr
from os import getenv
from paramiko import AutoAddPolicy, SSHClient
from dotenv import load_dotenv
import time

def main():
    load_dotenv()
    try:
        vars = load_environment_variables()
    except UnconfiguredEnvironment as e:
        exit(e)
    print(vars['JUMPHOST_IP'], vars['JUMPHOST_PORT'], vars['JUMPHOST_USER'], vars['JUMPHOST_PASS'])
    ssh_connection = establish_connection(vars['JUMPHOST_IP'], vars['JUMPHOST_PORT'], vars['JUMPHOST_USER'], vars['JUMPHOST_PASS'])
    command = 'sh ip int brief\n'
    execute_command(ssh_connection, command)
    close_connection(ssh_connection)

class UnconfiguredEnvironment(Exception):
    '''Exception class for unconfigured environment variables'''
    pass


def load_environment_variables() -> dict[str, str]:
    environment_variables_list = ['JUMPHOST_IP', 'JUMPHOST_PORT', 'JUMPHOST_USER', 'JUMPHOST_PASS']
    vars = dict()
    for var in environment_variables_list:
        if not (env_val := getenv(var, None)):
            raise UnconfiguredEnvironment(f"{var} is not configured")
        vars[var] = env_val
    return vars


def establish_connection(host:str, port:int, user:str, key:str) -> SSHClient:
    '''
    method used to establish a connection using the address, port, username and password
    return a established connection
    '''
    ssh_connection_pre = SSHClient()
    ssh_connection_pre.set_missing_host_key_policy(AutoAddPolicy())
    ssh_connection_pre.connect(hostname=host, port=port, username=user, password=key)
    ssh_connection = ssh_connection_pre.invoke_shell()
    print((ssh_connection.recv(65535)).decode("utf-8"))
    return ssh_connection


def execute_command(ssh_connection:SSHClient, command:str) -> None:
    '''
    method used to execute a command using a established connection, prints the output from the command
    '''
    ssh_connection.send(command)
    time.sleep(.5)
    print(ssh_connection.recv(65535).decode("utf-8"))
    


def close_connection(ssh_connection:SSHClient) -> None:
    '''
    method used to close a connection
    '''
    ssh_connection.close()


if __name__=="__main__":
    main()
