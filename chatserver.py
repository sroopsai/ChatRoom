import socket
import select
import sys
import re
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
CODE authored by S.ROOPSAI on 14/10/2018
"""
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 2:
    print("Correct usage: script, IP address:port number")
    sys.exit(1)
args = str(sys.argv[1]).split(':')
host = str(args[0])
port = int(args[1])
server.bind((host, port)) 
#binds the server to an entered IP address and at the specified port number. The client must be aware of these parameters
server.listen(100)
#listens for 100 active connections. This number can be increased as per convenience
list_clients = []
list_clients.append(server)
list_clients_temp = []
list_clients_perm = []
list_clients_perm_dict = {}
def broadcast(msg,conn):
	for sock in list_clients_perm:
		print('going to broadcasting')
		try:
				#print('broadcasting')
			sock.sendall(msg)
		except:
			sock.close()
			list_clients_perm.remove(sock)
			del list_clients_perm_dict[sock]
			list_clients.remove(sock)
while 1:
	readsock,writesock,errorsock = select.select(list_clients,[],[])
	for sock in readsock:
		if sock==server:
			newsock,addr = server.accept()
			newsock.sendall('Hello 1'.encode('ascii'))
		#	print(addr[0])
		#	print(readsock)
			list_clients.append(newsock)
			list_clients_temp.append(newsock)
		elif sock in list_clients_temp:
			try:
				nick = sock.recv(2048).decode('ascii')
				if nick:
					found = re.search(r'NICK\s(\S*)',nick)
					#print(found)
					name = str(found.group(1))
					
					if len(name)>12:
						sock.sendall('Error your nick name length should be less than 13 characters'.encode('ascii'))
					elif re.search(r'!',name) or re.search(r'@',name) or re.search(r'#',name) or re.search(r'\$',name) or re.search(r'%',name) or re.search(r'\^',name) or re.search(r'\*',name):
						sock.sendall('Error don\'t use special characters'.encode('ascii'))
					elif found:
						
						sock.sendall('Welcome to chat room '+str(name).encode('ascii'))
						list_clients_perm.append(sock)
						list_clients_perm_dict[sock] = name
					#	print(list_clients_perm_dict[sock])
						list_clients_temp.remove(sock)
					#	print(list_clients_temp)
					else:
						sock.sendall('Error bad command->Actual command:NICK <your-nick-name>'.encode('ascii'))
						
				else:
					sock.close()
					list_clients.remove(sock)
					list_clients_temp.remove(sock)
			except:
				continue
		elif sock in list_clients_perm:
			try:
				#print(sock)
				msg = sock.recv(2048).decode('ascii')
				if msg:
					found = re.search(r'MSG\s',msg)
					if len(msg)>259:
						sock.sendall('ERROR LENGTH OF THE MSG EXCEEDED->LIMIT:255 CHARACTERS')
					elif found:
						msg_to_send = str(list_clients_perm_dict[sock])+' '+str(msg[4:])
						broadcast(msg_to_send,sock)

					else:
						sock.sendall('ERROR BAD COMMAND->ACTUAL COMMAND:MSG <msg>'.encode('ascii'))
				else:
					sock.close()
					list_clients.remove(sock)
					list_clients_perm.remove(sock)
					del list_clients_perm_dict[sock]
			except:
				continue
server.close()