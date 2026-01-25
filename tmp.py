from customtkinter import *
from socket import *
import threading
import io
import base64
from PIL import Image

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")

        self.MENU_MAX_WIDTH = 200
        self.MENU_MIN_WIDTH = 40
        self.menu_speed = 15

        self.is_show_menu = True
        self.frame_width = self.MENU_MAX_WIDTH

        # ===== MENU FRAME =====
        self.frame_menu = CTkFrame(self, width=self.frame_width)
        self.frame_menu.pack_propagate(False)
        self.frame_menu.pack(side="left", fill="y")

        self.btn = CTkButton(
            self.frame_menu,
            text="◀️",
            width=40,
            height=40,
            command=self.toggle_show_menu
        )
        self.btn.pack(pady=5)

        self.label = CTkLabel(self.frame_menu, text="Say your name:", font=("Arial", 20))
        self.label.pack(pady=30)

        self.entry = CTkEntry(self.frame_menu, font=("Arial", 24))
        self.entry.pack()

        self.label_theme = CTkOptionMenu(
            self.frame_menu,
            values=["Dark", "Light"],
            command=self.change_theme,
            font=("Arial", 20)
        )
        self.label_theme.pack(pady=10)

        # ===== CHAT FRAME =====
        self.frame_chat = CTkFrame(self)
        self.frame_chat.pack(side="left", fill="both", expand=True)

        self.frame_chat.grid_rowconfigure(0, weight=1)
        self.frame_chat.grid_columnconfigure(0, weight=1)

        self.chat_text = CTkScrollableFrame(self.frame_chat)
        self.chat_text.grid(row=0, column=0, columnspan=2,
                            sticky="nsew", padx=5, pady=5)

        self.message_input = CTkEntry(
            self.frame_chat,
            placeholder_text="Message...",
            font=("Arial", 20)
        )
        self.message_input.grid(row=1, column=0,
                                sticky="ew", padx=5, pady=5)

        self.img_btn = CTkButton(self.frame_chat, text="📂", width=50,
                                height=40, command=self.open_image )
        self.img_btn.grid(row=1, column=1,
                                sticky="ew", padx=5, pady=5)

        self.send_btn = CTkButton(
            self.frame_chat,
            text="▶️",
            width=40,
            height=40,
            command=self.send_message
        )
        self.send_btn.grid(row=1, column=2, padx=5, pady=5)

        self.username = "Sasha"
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('192.168.1.14', 8080))
            hello = f"TEXT@{self.username}@[SYSTEM] {self.username} приєднався(лась) до чату \n"
            self.sock.send(hello.encode('utf-8'))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e: 
            self.add_message(f"Не вдалось підключитись до сервера: {e}")

    def toggle_show_menu(self):
        self.is_show_menu = not self.is_show_menu
        if self.is_show_menu:
            self.show_menu()
        else:
            self.close_menu()

    def show_menu(self):
        self.btn.configure(text="◀️")

        if self.frame_width < self.MENU_MAX_WIDTH:
            self.frame_width += self.menu_speed
            self.frame_menu.configure(width=self.frame_width)
            self.after(16, self.show_menu)
        else:
            self.label.pack(pady=30)
            self.entry.pack()
            self.label_theme.pack(pady=10)

    def close_menu(self):
        self.btn.configure(text="▶️")

        if self.frame_width == self.MENU_MAX_WIDTH:
            self.label.pack_forget()
            self.entry.pack_forget()
            self.label_theme.pack_forget()

        if self.frame_width > self.MENU_MIN_WIDTH:
            self.frame_width -= self.menu_speed
            self.frame_menu.configure(width=self.frame_width)
            self.after(16, self.close_menu)

    def change_theme(self, value):
        if value == "Dark":
            set_appearance_mode('dark')
        else:
            set_appearance_mode('light')

    def add_message(self, text, img=None):
        message_frame = CTkFrame(self.chat_text, fg_color="grey")
        message_frame.pack(pady=5, anchor="w")
        wrap_size = self.winfo_width() - self.frame_menu.winfo_width() - 40

        if not img:
            CTkLabel(message_frame, text=text, wraplength=wrap_size, text_color="white",
                    justify="left" ).pack(padx=10, pady=5)
        else:
            CTkLabel(message_frame, text=text, wraplength=wrap_size, 
                     text_color="white", image=img, compound='top', 
                     justify='left').pack(padx=10, pady=5)

    def send_message(self):
        self.username = self.entry.get()
        message = self.message_input.get()
        if message:
            self.add_message(message)
            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass

        self.message_input.delete(0, END)

    def recv_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                print(f"full chunk = {chunk}\n\n")
                if not chunk:
                    break
                buffer += chunk.decode()
                print(f"chunk = {chunk.decode()}\n\n")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
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
        elif msg_type == "IMAGE":
            if len(parts) >= 4:
                author =  parts[1]
                filename = parts[2]
                b64_img = parts[3]
                try:
                    img_data = base64.b64decode(b64_img)
                    pil_img = Image.open(io.BytesIO(img_data))
                    ctk_img = CTkImage(pil_img, size=(300, 300))
                    self.add_message(f"{author} send image: {filename}:", img=ctk_img)
                except Exception as e:
                    self.add_message(f"Помилка відображення зображення: {e}")
        else:
            self.add_message(line)

    def open_image(self):
        filename = filedialog.askopenfilename()
        if not filename:
            return
        try:
            with open(filename, "rb") as f:
                raw = f.read()
            b64_data = base64.b64encode(raw).decode()
            shortname = os.path.basename(filename)
            data = f"IMAGE@{self.username}@{shortname}@{b64_data}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
            self.add_message("", CTkImage(light_image=Image.open(filename), 
                                          size=(300, 300)))
        except Exception as e:
            self.add_message(f"Не вдалося відправити зображення: {e}")


win = MainWindow()
win.mainloop()
