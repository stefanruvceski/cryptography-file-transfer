import socket
import tqdm
import os
from time import sleep 
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append('C:/Users/Stefan/Downloads/Security/encryption/')
from file_encription import FileEncription
from key_generator import KeyGenerator

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# the ip address or hostname of the server, the receiver
host = "192.168.1.3"
# the port, let's use 5001
port = 5001
# the name of file we want to send, make sure it exists
filename = "mytext.txt"

key =  "9q6FWBTBO8WaW4tAoo3PfmHR-FxpLChynCD2XPChWzo=".encode()

file_enc = FileEncription(key)
enc_filename =  file_enc.encryptFile(filename)

# get the file size
filesize = os.path.getsize(enc_filename)

# create the client socket
s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

# send the filename and filesize
s.send(f"{enc_filename}{SEPARATOR}{filesize}".encode())

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {enc_filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(enc_filename, "rb+") as f:
    for _ in progress:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            continue
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
       
# close the socket
s.close()