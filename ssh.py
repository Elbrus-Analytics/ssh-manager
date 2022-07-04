from sys import stderr
from paramiko import AutoAddPolicy, SSHClient
import time

def main():
    hostname = '10.0.0.1'
    port = 22
    username = 'cisco'
    password = 'cisco'


    ssh_connection = establish_connection(hostname, port, username, password)
    command = 'sh ip int brief\n'
    execute_command(ssh_connection, command)
    close_connection(ssh_connection)


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
