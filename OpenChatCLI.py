import socket
import threading
import sys
import os

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
user = "Test Subject"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = f"{msg}".encode(FORMAT)
    msg_lenght = len(message)
    send_len = str(msg_lenght).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)


def mainMenu():
    global user
    print("----LocalChat----")
    print("Talk Locally.")
    print("------------v1.0-")
    print("Enter Your Name: ", end="")
    os.system("clear")
    sys.stdout.flush()
    user = input()


def recive():
    while True:
        sys.stdout.write("\033[s")
        sys.stdout.flush()
        chat = client.recv(1024).decode(FORMAT)
        if chat:
            sys.stdout.write('\033[u\033[1A\033[2K' + chat + '\n')
            sys.stdout.flush()


mainMenu()
threading.Thread(target=recive, daemon=True).start()
send(user)

while True:
    print("> ", end="")
    inp = input()
    send(inp)
    if inp == "!Q":
        break
