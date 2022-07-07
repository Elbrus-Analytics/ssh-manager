__author__ = 'Schmidt Tobias'
__version__=0.1

from os import getenv
from os.path import isdir
from os import mkdir
from paramiko import AutoAddPolicy, SSHClient
from dotenv import load_dotenv
import time
import psycopg2
from ipaddress import ip_address

#directory in which the output is stored
directory = '/home/elbrus/Desktop/ssh-manager/config/'
#address of current endpoint
address = None
#environment variables
vars = None

def main():  
    global vars

    #setup environment variables 
    load_dotenv()
    try:
        vars = load_environment_variables()
    except UnconfiguredEnvironment as e:
        exit(e)

    #connect to database
    connection = psycopg2.connect(
        database=vars['POSTGRES_DB'],
        user=vars['POSTGRES_USER'],
        password=vars['POSTGRES_PASS'],
        host=vars['POSTGRES_HOST'],
        port=vars['POSTGRES_PORT']
    )

    #fetch jobs from db
    with connection.cursor("ssh_device_cursor") as curs:
        curs.execute("""SELECT device_command.command, device.ip 
                        FROM device 
                        INNER JOIN device_command ON device.type=device_command.type;""")
        while (query := curs.fetchone()) is not None:
            #establish connection to target
            ssh = establish_connection_using_jumpserver(str(ip_address(query[1])), 'cisco', 'cisco')
            #execute and save command
            save_output(ssh, query[0])
    pass


class UnconfiguredEnvironment(Exception):
    '''Exception class for unconfigured environment variables'''
    pass

class MissingParameters(Execption):
    '''Exception class for missing parameters'''
    pass


def load_environment_variables() -> dict[str, str]:
    '''
    method used to load environment variables

    :return dict[str, str]: a dict where the environment variables name is mapped to the value
    '''
    environment_variables_list = ['JUMPSERVER_IP', 'JUMPSERVER_PORT', 'JUMPSERVER_USER', 'JUMPSERVER_PASS', 
    'POSTGRES_HOST', 'POSTGRES_USER', 'POSTGRES_PASS', 'POSTGRES_DB', 'POSTGRES_PORT',
    'SSH_KEYFILE']
    except_variable_list = ['JUMPSERVER_PASS', 'SSH_KEYFILE' ]
    vars = dict()
    for var in environment_variables_list:
        if not (env_val := getenv(var, None)):
            if not var in except_variable_list:
                raise UnconfiguredEnvironment(f'{var} is not configured')
        vars[var] = env_val
    return vars


def establish_connection_using_jumpserver(target:str, tuser:str=None, tkey:str=None, port:int=22) -> SSHClient:
    '''
    method used to connect to a target, using a jumphost inbetween
        -   connection to target uses username and password,
        -   connection to target uses ssh key stored on jumpserver

    :param str target: ip address of target
    :param str tuser: username to log into target
    :param str tkey: password to log into target
    :param int port: port to connect to

    :return SSHClient: ssh session with target
    '''
    #change depending on the operating system
    global address
    jumphost_ssh_connection = establish_connection_to_jumpserver()
    time.sleep(.5)
    jumphost_ssh_connection.send('ssh -l '+tuser+' -p '+str(port)+' '+target+'\n')
    jumphost_ssh_connection.recv(65535)
    time.sleep(2)
    if tkey:
        jumphost_ssh_connection.send(tkey+'\n')
        jumphost_ssh_connection.recv(65535)
        time.sleep(.5)
    address = target.replace('.','-')
    #!!!!!
    jumphost_ssh_connection.send('term len 0\n')
    time.sleep(.5)
    jumphost_ssh_connection.recv(65535)
    #!!!!!
    return jumphost_ssh_connection


def establish_connection_to_jumpserver() -> SSHClient:
    '''
    method used to establish a connection to the jumphost

    :return SSHClient: ssh session with target
    '''
    global vars
    if vars['SSH_KEYFILE'] and vars['JUMPSERVER_PASS']:
        ssh_connection = establish_connection(host=vars['JUMPSERVER_IP'], user=vars['JUMPSERVER_USER'], key=vars['JUMPSERVER_PASS'],
        keyfile=vars['SSH_KEYFILE'], port=vars['JUMPSERVER_PORT'])
    elif vars['SSH_KEYFILE']:
        ssh_connection = establish_connection(host=vars['JUMPSERVER_IP'], key_filename=vars['SSH_KEYFILE'], port=vars['JUMPSERVER_PORT'])
    elif vars['JUMPSERVER_PASS']:
        ssh_connection = establish_connection(host=vars['JUMPSERVER_IP'], user=vars['JUMPSERVER_USER'], key=vars['JUMPSERVER_PASS'],
        port=vars['JUMPSERVER_PORT'])
    else:
        raise MissingParameters(f'.var must contain atleast one value for either  \'JUMPSERVER_PASS\' or \'SSH_KEYFILE\'!')
    return ssh_connection


def establish_connection(host:str, user:str, key:str=None, keyfile:str=None, port:int=22) -> SSHClient:
    '''
    method used to establish a connection using the address, port, username and password
    return a established connection

    :param str host: IP-Address of the target
    :param str user: username to log into the target
    :param str key: password to log into the target
    :param int port: port to connect to
    :param str keyfile: keyfile to use for connection

    :return SSHClient: ssh session with target
    '''
    global address
    address = host.replace('.','-')
    ssh_connection_pre = SSHClient()
    ssh_connection_pre.set_missing_host_key_policy(AutoAddPolicy())
    if keyfile and key:
        ssh_connection_pre.connect(hostname=host, port=port, username=user, password=key, key_filename=keyfile)
    elif keyfile:
        ssh_connection_pre.connect(hostname=host, key_filename=keyfile)
    elif key:
        ssh_connection_pre.connect(hostname=host, port=port, username=user, password=key)
    else:
        raise MissingParameters(f'parameter must contain atleast one value for either  \'key\' or \'keyfile\'!')
    ssh_connection = ssh_connection_pre.invoke_shell()
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
    global address, directory
    response = execute_command(ssh_connection, command, readsize)
    path = directory+address
    print(address)
    if not isdir(path):
        mkdir(path)
    path +='/'+command.replace(' ','-')+'.txt'
    file = open(path, 'w')
    file.write(response)
    file.close()


if __name__=="__main__":
    main()
