import socket
from termcolor import colored

def scan(ipaddress, port):
    try:
        sock = socket.socket()
        sock.connect((ipaddress, port))
        serviceVersion = sock.recv(1024)
        serviceVersion = serviceVersion.decode('utf-8')
        serviceVersion = serviceVersion.strip('\n')
        portstate = f'Port {str(port)} is open'
        print(colored(portstate, 'green'), end='   ')
        print(serviceVersion)
    except ConnectionRefusedError:
        print(colored(f'Port {str(port)} is close', 'red'))
    except UnicodeDecodeError:
        print(colored(f'Port {str(port)} is open', 'green'))


target = input('Target: ')
ports = input('Port: ')

if ',' in ports:
    port_list = ports.split(',')
    for i in port_list:
        scan(target, int(i))
elif '-' in ports:
    portRange = ports.split('-')
    start = int(portRange[0])
    end = int(portRange[1])
    for i in range(start, end+1):
        scan(target, i)
else:
    scan(target, int(ports))

