# client.py

import socket
# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

#get local machine name host is the ip address.
host = socket.gethostname();
port = 9999;

#connection to hostname on the port.
s.connect((host, port))

# Recieve no more than 1024 bytes
data = s.recv(1024);

s.close();

print(data.decode('ascii'));
