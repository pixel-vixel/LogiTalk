from customtkinter import *

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")

        #frame menu
        self.frame_menu = CTkFrame(self, width=200, height=self.winfo_height())
        self.frame_menu.pack_propagate(False)
        self.frame_menu.configure(width=200)
        self.frame_menu.place(x=0, y=0)
        
        self.is_show_menu = True
        self.frame_width = 200

        self.btn = CTkButton(self.frame_menu, text="◀️", width=40, height=40, command=self.toggle_show_menu)
        self.btn.pack()
        self.menu_speed = 10

        self.label = CTkLabel(self.frame_menu, text="Say your name: ")
        self.label.pack(pady=30)

        self.entry = CTkEntry(self.frame_menu)
        self.entry.pack()

        self.label_theme = CTkOptionMenu(self.frame_menu, values=['Dark', 'Light'])
        self.Theme = None
        self.label_theme.pack()

        #frame chat
        self.frame_chat = CTkFrame(self, height=self.winfo_height(), width=200)
        self.frame_chat.pack_propagate(False)
        self.frame_chat.place(x=200, y=0)

        self.chat_text = CTkTextbox(self.frame_chat, state='disable')
        self.chat_text.grid(row=0, column=0, columnspan=2)

        self.message_input = CTkEntry(self.frame_chat, placeholder_text="Message...", 
                                      width=self.frame_chat.winfo_width()-50)
        self.message_input.grid(row=9, column=0)

        self.send_btn = CTkButton(self.frame_chat, text='▶️', width=40, height=40)
        self.send_btn.grid(row=9, column=1)

    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.frame_chat.configure(width=390, height=self.winfo_height())
            self.chat_text.configure(width=390)
            self.message_input.configure(width=330)
            self.close_menu()
        else:
            self.is_show_menu = True
            self.frame_chat.configure(width=200, height=self.winfo_height())
            self.chat_text.configure(width=200)
            self.message_input.configure(width=160)
            self.show_menu()

    def show_menu(self):
        self.btn.configure(text='◀️') 
        self.label.pack(pady=30)
        self.entry.pack()
        self.label_theme.pack()
        if self.frame_width <= 200:
            self.frame_width += self.menu_speed
            self.frame_menu.configure(width=self.frame_width, height=self.winfo_height())
            self.frame_chat.place_configure(x=self.frame_width)
                
        if self.is_show_menu:
            self.after(10, self.show_menu)

    def close_menu(self):
        self.btn.configure(text='▶️')
        self.label.pack_forget()
        self.entry.pack_forget()
        self.label_theme.pack_forget()
        if self.frame_width >= 40:
            self.frame_width -= self.menu_speed 
            self.frame_menu.configure(width=self.frame_width, height=self.winfo_height())
            self.frame_chat.place_configure(x=self.frame_width)
        if not self.is_show_menu:
            self.after(10, self.close_menu)

win = MainWindow()
win.mainloop()