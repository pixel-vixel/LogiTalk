from customtkinter import *
from socket import *
import threading
import io
import base64
from PIL import Image

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("LogiTalk")

        self.username = "Sasha"
        self.is_show_menu = False
        self.anim_speed = -20

        # === menu frame ===
        self.frame_menu = CTkFrame(self, width=300, corner_radius=0, fg_color="#153B50")
        self.frame_menu.pack_propagate(False)
        self.frame_menu.pack(side=LEFT, fill="y")

            # button to open/close menu
        self.menu_btn = CTkButton(self.frame_menu, 
                                  width=60, height=60, text="🟰", 
                                  command=self.toggle_show_menu)
        self.menu_btn.pack(padx=0)

            # avatar image label 
        self.avatar = CTkLabel(self.frame_menu, width=100, height=100, fg_color="#DADFF7", text='image')
        self.avatar.pack(pady=50)

            # button for avatar selection
        self.avatar_btn = CTkButton(self.frame_menu, width=150, height=30, 
                                    fg_color="#429EA6", text="Виберіть аватар",
                                    text_color="#DADFF7")
        self.avatar_btn.pack()

            # entry for username
        self.username_entry = CTkEntry(self.frame_menu, width=200, height=30, 
                                       fg_color="#2F6F75", text_color="#DADFF7", 
                                       placeholder_text="Enter name")
        self.username_entry.pack(pady=20)

            # button for name
        self.username_btn = CTkButton(self.frame_menu, width=150, height=30, 
                                    fg_color="#429EA6", text="Підтвердити ім'я",
                                    text_color="#DADFF7", command=self.save_name)
        self.username_btn.pack()

        # === chat frame ===
        self.frame_chat = CTkFrame(self, width=500, corner_radius=0)
        self.frame_chat.pack_propagate(False)
        self.frame_chat.pack(side=LEFT, fill='both', expand=True)

        self.frame_chat.grid_rowconfigure(0, weight=1)
        self.frame_chat.grid_columnconfigure(0, weight=1)

            # scroll frame for chat
        self.chat = CTkScrollableFrame(self.frame_chat)
        self.chat.grid(row=0, column=0, columnspan=3,
                            sticky="nsew", padx=5, pady=5)
        
            # message input
        self.message = CTkEntry(self.frame_chat, placeholder_text="Message...", font=("Arial", 20))
        self.message.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

            # button for image
        self.img_btn = CTkButton(self.frame_chat, text="📂", width=50, height=40)
        self.img_btn.grid(row=1, column=1,
                                sticky="ew", padx=5, pady=5)
            # send btn
        self.send_btn = CTkButton(
            self.frame_chat,
            text="▶️",
            width=40,
            height=40,
            command=self.send_message
        )
        self.send_btn.grid(row=1, column=2, padx=5, pady=5)

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('localhost', 8080))
            hello = f"TEXT@{self.username}@ [SYSTEM] {self.username} приєднався(лась) до чату!\n"
            self.sock.send(hello.encode('utf-8'))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            self.add_message(f"Не вдалось під'єднатись: {e}")

    def toggle_show_menu(self):
        self.is_show_menu = not self.is_show_menu
        self.anim_speed *= -1
        if self.is_show_menu:
            self.show_menu()
        else:
            self.show_menu()

    def show_menu(self):
        self.frame_menu.configure(width=self.frame_menu.winfo_width() + self.anim_speed)
        if not self.frame_menu.winfo_width() >= 300 and self.is_show_menu:
            self.after(10, self.show_menu)

            self.avatar.pack(pady=50)
            self.avatar_btn.pack()
            self.username_entry.pack(pady=20)
            self.username_btn.pack()

        elif self.frame_menu.winfo_width() >= 100 and not self.is_show_menu:
            self.after(10, self.show_menu)

            if self.avatar:
                self.avatar.pack_forget()
            if self.avatar_btn:
                self.avatar_btn.pack_forget()
            if self.username_btn:
                self.username_btn.pack_forget()
            if self.username_entry:
                self.username_entry.pack_forget()

    def save_name(self):
        new_name = self.username_entry.get().strip()
        if new_name:
            self.username = new_name

    def add_message(self, text, is_me=False, img=None):
        message_frame = CTkFrame(self.chat, fg_color=("green" if is_me else "blue"))
        message_frame.pack(pady=5, anchor=("w" if not is_me else "e"))
        wrap_size = self.winfo_width() - self.frame_menu.winfo_width() - 60

        CTkLabel(message_frame, text=text, wraplength=wrap_size, text_color="white",
                justify="left" ).pack(padx=10, pady=5)

    def send_message(self):
        message = self.message.get()
        if message:
            self.add_message(f"{message}")
            data = f"TEXT@{self.username}@{message}"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
        self.message.delete(0, END)

    def recv_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode('utf-8', errors='ignore')

                while "\n" in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self.handle_line(line.strip())
            except:
                break
        self.sock.close()

    def handle_line(self, line):
        if not line:
            return
        parts = line.split("@", 3)
        msg_type = parts[0]
        if msg_type == "TEXT":
            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]
                self.add_message(f"{author}: {message}")

win = MainWindow()
win.mainloop()