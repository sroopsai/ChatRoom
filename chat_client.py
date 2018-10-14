import socket
import select
import sys

server = socket.socket()

if len(sys.argv) != 2:
    print "Correct usage: script, IP address, port number"
    sys.exit(1)
args = str(sys.argv[1]).split(':')
host = str(args[0])
port = int(args[1])
server.connect((host, port))

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
                server.sendall(message.encode('ascii'))
            
            
server.close()