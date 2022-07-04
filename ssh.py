from paramiko import AutoAddPolicy, SSHClient
import time

hostname = '10.0.0.1'
port = 22
username = 'cisco'
password = 'cisco'

command = 'show ip int brief \n'

ssh_connection = SSHClient()
ssh_connection.set_missing_host_key_policy(AutoAddPolicy())
ssh_connection.connect(hostname=hostname, port=port, username=username, password=password)


stdin, stdout, stderr = ssh_connection.exec_command(command)
stdin.close()
output = stdout.readlines()
print(' '.join(map(str, output)))

ssh_connection.close()
print("working")