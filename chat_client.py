import socket
import select
import sys
import re
''' 
Code authored by Roop Sai S
This program is client side code which is written following this protocol-->
                sending connection request
    client    ------------------------>      server
              <------------------------
        sends  Hello 1 (connection established)

                sends NICK <nick>
    client    ------------------------>      server
              <------------------------
            sends Welcome to Chat room <nick>/Error msg
                sends MSG <msg1>                        sends MSG <msg2>
    client1   ------------------------>      server   <------------------- client2 
              if error sends error msg                if error sends error msg
              <------------------------               ------------------->
              <------------------------               ------------------->
            sends MSG <client2-nick>: <msg2>         sends MSG <client1-nick>: <msg1>
'''
server = socket.socket()
if len(sys.argv) != 3:
    print ("For Linux terminals --> python chatclient.py serveripaddr:portnum nickname")
    sys.exit(1)
args = str(sys.argv[1]).split(':')
host = str(args[0])
port = int(args[1])
nick = str(sys.argv[2])
server.connect((host, port))
hello = server.recv(1024).decode('ascii')
print(hello)
server.sendall(('NICK '+nick).encode('ascii'))
ok = server.recv(1024).decode('ascii')
if re.search('Error',ok) or re.search('ERROR',ok):
    print(ok)
    sys.exit()
print(ok)
while True:
    sockets = [sys.stdin, server]
    read_sockets,write_sockets, error_sockets = select.select(sockets, [], [])
    for sock in read_sockets:
        if sock == server:
            message = sock.recv(2048).decode('ascii')
            if re.search(r'Error',message) or re.search(r'ERROR',message):
                print (message)
            else:
                message = message[4:]#stripping the message removing MSG and giving it to print out as per the protocol
                print (message)
        else:
            message = sys.stdin.readline()
            if message == '\n':
                continue
            else:
                server.sendall(('MSG '+message).encode('ascii'))
server.close()
