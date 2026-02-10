import customtkinter as ctk
import socket
import threading

# const Network vals
SERV = "127.0.0.1"
PORT = 5050
ADDR = (SERV, PORT)
HEADER = 64
FORMAT = "utf-8"

# CTk Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
ctk.deactivate_automatic_dpi_awareness()
ctk.set_widget_scaling(1.25)
ctk.set_window_scaling(1.25)


# Main classes


class Gui(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x600")
        self.title("OpenChat")

        ctk.CTkLabel(self, text="Hello World!").place(
            relx=0.5, rely=0.5, anchor="center")

        self.mainloop()


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

    def send(self, msg):
        message = f"{msg}".encode(FORMAT)
        msg_lenght = len(message)
        send_len = str(msg_lenght).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        self.client.send(send_len)
        self.client.send(message)

    def recive(self):
        while True:
            chat = self.client.recv(1024).decode(FORMAT)
            if chat:
                return chat


if __name__ == "__main__":
    Gui()
