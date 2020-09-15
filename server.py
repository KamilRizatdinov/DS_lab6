from os import path
import socket
from threading import Thread

BUFFER_SIZE = 1024


class ClientListener(Thread):
    def __init__(self, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock

    def _copy_file(self, filename):
        if path.exists(filename):

            dot_position = filename.find('.')
            filename_body = filename[: dot_position]
            filename_tail = filename[dot_position: ]
            counter = 1

            while True:
                if path.exists(f'{filename_body}_copy{counter}{filename_tail}'):
                    counter += 1
                else: 
                    return f'{filename_body}_copy{counter}{filename_tail}'
        else:
            return filename

    def run(self):
        # First we need to get the lenght of the filename in bytes
        # 3 bytes are enough to describe filename lenght since on linux maximum filename is 255 bytes
        filename_length = self.sock.recv(3).decode()
        self.sock.send(b'Filename length recieved!')

        # Next, we want to get the filename itself, if this file already exist - make a copy
        filename = self._copy_file(self.sock.recv(int(filename_length)).decode())
        self.sock.send(b'Filename recieved!')

        # Recieving the file data
        with open(filename, 'wb') as f:
            while True:
                data = self.sock.recv(BUFFER_SIZE)
                if data:
                    f.write(data)
                else:
                    self.sock.close()
                    print("Connection closed!")
                    return

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 8800))
    sock.listen()
    
    while True:
        con, addr = sock.accept()
        print(f"Connection with {addr} established!")
        ClientListener(con).start()


if __name__ == "__main__":
    main()