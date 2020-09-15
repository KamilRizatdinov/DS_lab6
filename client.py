import os
import socket
import sys
import time

from tqdm import tqdm


BUFFER_SIZE = 1024

# Getting the arguments from command line
filename, ip, port = sys.argv[1:]

# Creating and connecting to the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, int(port)))

# Sending the filename data
sock.send(str.encode(f'{len(filename):03d}'))  # Filename length
sock.send(str.encode(filename))  # Filename itself

pbar = tqdm(total=os.path.getsize(filename))

# Sending the file data
f = open(filename, 'rb')
while True:
    data = f.read(BUFFER_SIZE)
    if data:
        sock.send(data)
        pbar.update(BUFFER_SIZE)
    else:
        f.close()
        break

pbar.close()
# Closing the socket connection
print('Successfully send the file')
# sock.close()
print('Connection closed')
