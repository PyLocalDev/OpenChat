import customtkinter as ctk
import tkinter as tk
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

        ctk.CTkLabel(
            self, text="OpenChat - Chat Freely!", font=("hack", 18)).place(anchor="nw", x=15, y=10)

        self.textbox = ctk.CTkTextbox(
            master=self, width=600, height=400, corner_radius=0)
        self.textbox.place(anchor="center", relx=0.5, rely=0.5)
        self.textbox.insert("0.0", "<OpenChat> Hello This is OpenChat!\n")
        self.textbox.insert("0.0", "<PyLocalDev> And I'm Creator of it!\n")

        self.chatVar = tk.Variable(self)
        chat = ctk.CTkEntry(self, textvariable=self.chatVar, width=200)
        chat.place(anchor="sw", relx=0.15, rely=0.90)
        ctk.CTkButton(self, text="Send", command=self.test).place(
            anchor="se", relx=0.8, rely=0.9)
        self.mainloop()

    def test(self):
        self.textbox.insert("0.0", self.chatVar.get() + "\n")


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


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox.place(anchor="center", relx=0.5, rely=0.5)
        self.textbox.insert("0.0", "Some example text!\n" * 50)

        self.mainloop()


if __name__ == "__main__":
    Gui()
