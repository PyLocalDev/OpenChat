import socket
import threading

# Global Varibles
HEADER = 64
SERVER = "127.0.0.1"
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
clients = []
lock = threading.Lock()


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)

        print("-------OpenChat---v1.0")
        print("[SERVER] Server has started...")
        self.start()

    def handle_client(self, conn, addr):

        clients.append(conn)
        usr_len = conn.recv(HEADER).decode(FORMAT)
        if usr_len:
            usr_len = int(usr_len)
            usr = conn.recv(usr_len).decode(FORMAT)
        connected = True
        print(f"[SERVER] {usr} Has Joined the Chat. =D")

        while connected:
            msg_len = conn.recv(HEADER).decode(FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                msg = conn.recv(msg_len).decode(FORMAT)
                if msg == "!Q":
                    connected = False
                chat = f"<{usr}> {msg}"
                print(chat)

                with lock:
                    for client in clients:
                        if client != conn:
                            try:
                                client.sendall(chat.encode(FORMAT))
                            except:
                                pass

        print(f"[SERVER] {usr} Has disconnected. =(")
        print(f"[SERVER] There are {
              threading.active_count() - 2} in this Chat.")
        conn.close()

    def start(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(
                target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[SERVER] There are {
                  threading.active_count() - 1} in this chat.")


if __name__ == "__main__":
    Server()
