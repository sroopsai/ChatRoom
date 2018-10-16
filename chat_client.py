import socket
import select
import sys

import re

server = socket.socket()

if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number, NICKNAME"
    sys.exit(1)
args = str(sys.argv[1]).split(':')
host = str(args[0])
port = int(args[1])
nick = str(sys.argv[2])
server.connect((host, port))
hello = server.recv(1024).decode('ascii')
server.sendall('NICK '+nick.encode('ascii'))
ok = server.recv(1024).decode('ascii')
while not re.search(r'Welcome to chat room\s\w*',ok):
	print(ok)
	nick = input('Enter your name: ')
	try:
		server.sendall('NICK '+nick.encode('ascii'))
		ok = server.recv(1024).decode('ascii')
	except:
		continue
print(ok)



while True:
    sockets = [sys.stdin, server]
    read_sockets,write_sockets, error_sockets = select.select(sockets, [], [])
    for sock in read_sockets:
        if sock == server:
            message = sock.recv(2048).decode('ascii')
            print message
        else:
            message = sys.stdin.readline()
            if message == '\n':
                continue
            else:
                server.sendall('MSG '+message.encode('ascii'))
            
            
server.close()