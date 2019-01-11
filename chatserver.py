import socket
import sys
import re
import select
#select module doesn't work in windows environment but will work in cygwin terminal 
#this program  works in linux terminals 
''' 
Code authored by Roop Sai S
This program is server side code which is written following this protocol-->
                sending connection request
    client    ------------------------>      server
              <------------------------
        sends  Hello 1 (connection established)/Connection failed msg

                sends NICK <nick>
    client    ------------------------>      server
              <------------------------
            sends Welcome to Chat room <nick>/Error msg

    Server acting as mediator between all n clients and broadcasts the message from one client to all other n-1 clients
    except to client the message received from.

                sends MSG <msg1>                        sends MSG <msg2>
    client1   ------------------------>      server   <------------------- client2 
              if error sends error msg         ^       if error sends error msg
              <------------------------        |       ------------------->
              <------------------------        |     ------------------->
            sends MSG <client2-nick>: <msg2>   |      sends MSG <client1-nick>: <msg1>
                                               |
                                               |
                                               |
                                            client3

'''
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
if (len(sys.argv)!=2):
    print("Correct Usage for linux terminals-> python3 chatserver.py serv_addr:port_num")
args = str(sys.argv[1]).split(':')
host = str(args[0])
port = int(args[1])
server.bind((host,port))
server.listen(100)
list_clients=[]
list_clients.append(server)
list_clients_temp=[]
list_clients_perm=[]
list_clients_perm_dict={}
def broadcast(msg,conn):
    for sock in list_clients_perm:
        if sock!=conn:
            print('broadcasting')
            try:
                sock.sendall(msg.encode('ascii'))
            except:
                sock.close()
                list_clients_perm.remove(sock)
                del list_clients_perm_dict[sock]
                list_clients.remove(sock)
def main():
    print('chat server running')
    while True:
        readsock,writesock,errorsock=select.select(list_clients,[],[])
        for sock in readsock:
            if sock==server:
                newsock,addr=server.accept()
                newsock.sendall('Hello 1'.encode('ascii'))
                list_clients.append(newsock)
                list_clients_temp.append(newsock)
            elif sock in list_clients_temp:
                try:
                    nick=sock.recv(1024).decode('ascii')
                    if nick:
                        found=re.search(r'NICK\s(\S*)',nick)
                        name=str(found.group(1))
                        if len(name)>12:
                            sock.sendall('Error your nick name length should be less than 13 characters'.encode('ascii'))
                        elif re.search(r'!',name) or re.search(r'@',name) or re.search(r'#',name) or re.search(r'\$',name) or re.search(r'%',name) or re.search(r'\*',name) or re.search(r'\^',name):
                            sock.sendall('Error don\'t use special characters in your nick names'.encode('ascii'))
                        elif found:
                            sock.sendall(('Welcome to chat room '+str(name)).encode('ascii'))
                            list_clients_perm.append(sock)
                            list_clients_perm_dict[sock]=name
                            list_clients_temp.remove(sock)
                        else:
                            sock.sendall('Error -> BAD COMMAND ACTUAL COMMAND PROTOCOL NICK <nick>'.encode('ascii'))
                    else:
                        sock.close()
                        list_clients.remove(sock)
                        list_clients_temp.remove(sock)
                except:
                    continue
            elif sock in list_clients_perm:
                try:
                    msg=sock.recv(1024).decode('ascii')
                    if msg:
                        found=re.search(r'MSG\s',msg)
                        if len(msg)>259:
                            sock.sendall('Error message length should not exceed 256 characters'.encode('ascii'))
                        elif found:
                            msg_to_send='MSG '+str(list_clients_perm_dict[sock])+': '+msg[4:]
                            broadcast(msg_to_send,sock)
                        else:
                            sock.sendall('Error BAD COMMAND ACTUAL COMMAND MSG <msg>'.encode('ascii'))
                    else:
                        sock.close()
                        list_clients.remove(sock)
                        list_clients_perm.remove(sock)
                        del list_clients_perm_dict[sock]
                except:
                    continue
    server.close()
if __name__ == "__main__":
    main()
    

