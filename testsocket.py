import socket
from game import *
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 12321))

comm=Communicator(s)
comm.print('Ping\r\n')
s=comm.read_line()
print(s)