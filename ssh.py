from paramiko import AutoAddPolicy, SSHClient
import time

def main():
    hostname = '10.0.0.1'
    port = 22
    username = 'cisco'
    password = 'cisco'

    command = 'show ip int brief \n'

    ssh_connection = establish_connection(hostname, port, username, password)
    execute_command(ssh_connection, command)
    close_connection(ssh_connection)


def establish_connection(host:str, port:int, user:str, key:str) -> SSHClient:
    ssh_connection = SSHClient()
    ssh_connection.set_missing_host_key_policy(AutoAddPolicy())
    ssh_connection.connect(hostname=host, port=port, username=user, password=key)
    return ssh_connection


def execute_command(ssh_connection:SSHClient, command:str) -> None:
    stdin, stdout, stderr = ssh_connection.exec_command(command)
    stdin.close()
    output = stdout.readlines()
    print(' '.join(map(str, output)))


def close_connection(ssh_connection:SSHClient) -> None:
    ssh_connection.close()


if __name__=="__main__":
    main()
