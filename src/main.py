from audioop import add
from os import getenv
from os.path import isdir
from os import mkdir
from paramiko import AutoAddPolicy, SSHClient
from datetime import date
from dotenv import load_dotenv
import time

directory = '../config/'
address = None

def main():  
    ssh_connection = establish_connection_using_jumphost('14.14.14.28', 'cisco', 'cisco')
    save_output(ssh_connection, 'sh ip prot')
    close_connection(ssh_connection)
    ssh_connection = establish_connection_to_jumphost()
    save_output(ssh_connection, 'sh ip prot')
    close_connection(ssh_connection)
    pass


class UnconfiguredEnvironment(Exception):
    '''Exception class for unconfigured environment variables'''
    pass


def load_environment_variables() -> dict[str, str]:
    '''
    method used to load environment variables

    :return dict[str, str]: a dict where the environment variables name is mapped to the value
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

    :param str target: ip address of target
    :param str tuser: username to log into target
    :param str tkey: password to log into target
    :param int port: port to connect to

    :return SSHClient: ssh session with target
    '''
    global address
    jumphost_ssh_connection = establish_connection_to_jumphost()
    time.sleep(.5)
    jumphost_ssh_connection.send('ssh -l '+tuser+' -p '+str(port)+' '+target+'\n')
    jumphost_ssh_connection.recv(65535)
    time.sleep(2)
    jumphost_ssh_connection.send(tkey+'\n')
    jumphost_ssh_connection.recv(65535)
    time.sleep(.5)
    address = target.replace('.','-')
    #!!!!!
    jumphost_ssh_connection.send('term len 0\n')
    #!!!!!
    return jumphost_ssh_connection


def establish_connection_to_jumphost() -> SSHClient:
    '''
    method used to establish a connection to the jumphost

    :param boolean mute: set True to mute the output 

    :return SSHClient: ssh session with target
    '''
    load_dotenv()
    try:
        vars = load_environment_variables()
    except UnconfiguredEnvironment as e:
        exit(e)
    ssh_connection = establish_connection(vars['JUMPHOST_IP'], vars['JUMPHOST_USER'], vars['JUMPHOST_PASS'], vars['JUMPHOST_PORT'])
    return ssh_connection


def establish_connection(host:str, user:str, key:str, port=22) -> SSHClient:
    '''
    method used to establish a connection using the address, port, username and password
    return a established connection

    :param str host: IP-Address of the target
    :param str user: username to log into the target
    :param str key: password to log into the target
    :param int port: port to connect to
    :param boolean mute: set True to mute the output

    :return SSHClient: ssh session with target
    '''
    global address
    address = host.replace('.','-')
    ssh_connection_pre = SSHClient()
    ssh_connection_pre.set_missing_host_key_policy(AutoAddPolicy())
    ssh_connection_pre.connect(hostname=host, port=port, username=user, password=key)
    ssh_connection = ssh_connection_pre.invoke_shell()
    #!!!!!
    ssh_connection.send('term len 0\n')
    #!!!!!
    return ssh_connection


def execute_command(ssh_connection:SSHClient, command:str, readsize=65535) -> str:
    '''
    method used to execute a command using a established connection, prints the output from the command

    :param SSHClient ssh_connection: active ssh connection to a target
    :param str command: command to execute
    :param int readsize: how many bytes of the response are read

    :return str: the response the the comand decoded in 'utf-8'
    '''
    ssh_connection.send(command+'\n')
    time.sleep(10)
    return ssh_connection.recv(readsize).decode("utf-8")
    


def close_connection(ssh_connection:SSHClient) -> None:
    '''
    method used to close a connection

    :param SSHClient ssh_connection: active ssh connection to a target
    '''
    ssh_connection.close()


def save_output(ssh_connection:SSHClient, command:str, readsize=65535) -> None:
    '''
    method used to execute a command and save its output to a file, following the naming format "hostname-YYYY-MM-DD.txt" for the output file

    :param SSHClient ssh_connection: active ssh connection to a target
    :param str command: command to execute
    :param int readsize: how many bytes of the response are read
    '''
    global address
    response = execute_command(ssh_connection, command, readsize)
    path = directory+address
    print(path)
    if not isdir(path):
        mkdir(path)
    path +='/'+command.replace(' ','-')+'.txt'
    file = open(path, 'w')
    file.write(response)
    file.close()


if __name__=="__main__":
    main()
