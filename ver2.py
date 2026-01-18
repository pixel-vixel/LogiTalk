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

        # === menu frame ===
        self.frame_menu = CTkFrame(self, width=300, corner_radius=0, fg_color="#153B50")
        self.frame_menu.pack_propagate(False)
        self.frame_menu.pack(side=LEFT, fill="y")

            # button to open/close menu
        self.menu_btn = CTkButton(self.frame_menu, width=60, height=60, text="🟰")
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
                                    text_color="#DADFF7")
        self.username_btn.pack()

        # === chat frame ===
        self.frame_chat = CTkFrame(self, width=500, corner_radius=0)
        self.frame_chat.pack_propagate(False)
        self.frame_chat.pack(side=RIGHT, fill='y')

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
            height=40
        )
        self.send_btn.grid(row=1, column=2, padx=5, pady=5)


win = MainWindow()
win.mainloop()