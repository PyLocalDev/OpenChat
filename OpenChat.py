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
usr = None

# CTk Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# ctk.deactivate_automatic_dpi_awareness()
ctk.set_widget_scaling(1.25)
ctk.set_window_scaling(1.25)


# Main classes

class Name(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Enter Your Name - OpenChat")
        self.geometry("600x200")

        self.nameVar = tk.StringVar(self)

        ctk.CTkLabel(self, text="Enter Your Name:").place(
            anchor="nw", relx=0.3, rely=0.3)
        ctk.CTkEntry(self, textvariable=self.nameVar).place(
            anchor="w", relx=0.3, rely=0.5)

        ctk.CTkButton(self, text="Ok", command=self.launch).place(
            anchor="w", relx=0.2, rely=0.8)
        ctk.CTkButton(self, text="Quit", command=lambda: exit(0)
                      ).place(anchor="e", relx=0.8, rely=0.8)

        self.mainloop()

    def launch(self):
        global usr
        usr = self.nameVar.get()
        self.destroy()
        Gui()


class Gui(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x600")
        self.title("OpenChat")

        self.cli = Client()

        self.cli.send(usr)  # Sends username

        threading.Thread(target=self.recv, daemon=True).start()

        ctk.CTkLabel(
            self, text="OpenChat - Chat Freely!", font=("hack", 18)).place(anchor="nw", x=15, y=10)

        self.textbox = ctk.CTkTextbox(
            master=self, width=600, height=400, corner_radius=0, font=("hack", 14))
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
        if self.chatVar.get() == "!Q":
            self.cli.send(self.chatVar.get())
            self.cli.disconn()
            exit(0)
        else:
            self.cli.send(self.chatVar.get())

    def recv(self):
        while True:
            chat = self.cli.recive()
            self.textbox.insert("0.0", chat + "\n")


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
        chat = self.client.recv(1024).decode(FORMAT)
        if chat:
            return chat

    def disconn(self):
        self.client.close()


if __name__ == "__main__":
    Name()
