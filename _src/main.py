import customtkinter as ctk
import tkinter as tk
import subprocess as sb
from tkinter import messagebox
from PIL import Image

class Mainpage:
    def __init__(self, master):
        self.master = master
        self.Setup()
    
    def Setup(self):
        self.Frames()
        self.Buttons()
        self.Labels()
        
    def Frames(self):
        self.height = screeen.winfo_screenheight()
        self.width = screeen.winfo_screenwidth()
        self.f_screen = ctk.CTkFrame(self.master, width=200, height=self.height, fg_color='green')
        self.f_screen.pack(side=tk.LEFT)
        
        self.f_screen_main = ctk.CTkFrame(self.master, width=self.width, height=self.height, fg_color='white')
        self.f_screen_main.pack(side=tk.TOP)

    def Labels(self):
        self.l_main_title = ctk.CTkLabel(self.f_screen_main, text='SEU BANCO EXCLUSIVO DE CARTÕES DIGITAIS', font=('Fixedsys', 32, 'bold'), text_color='#000000', fg_color='gray')
        self.l_main_title.pack(side=tk.TOP, expand=True)
                
    def Buttons(self):
        self.btn_add_card = ctk.CTkButton(self.f_screen, text='Adicionar', fg_color='green', text_color='white', font=('Arial', 15, 'bold'), hover=False, command=self.Open_add_screen) 
        self.btn_add_card.place(x=20, y=50)
        
        self.btn_vizu_card = ctk.CTkButton(self.f_screen, text='Vizualizar', fg_color='green', text_color='white', font=('Arial', 15, 'bold'), hover=False, command=self.Open_vizu_screen) 
        self.btn_vizu_card.place(x=20, y=100)
        
        self.btn_edit_card = ctk.CTkButton(self.f_screen, text='Editar', fg_color='green', text_color='white', font=('Arial', 15, 'bold'), hover=False, command=self.Open_edit_screen) 
        self.btn_edit_card.place(x=20, y=150)
        
        self.btn_quit = ctk.CTkButton(self.f_screen, text='sair', fg_color='green', text_color='white', font=('Arial', 15, 'bold'), hover=False, command=self.Quit) 
        self.btn_quit.place(x=20, y=200)
        
    def Open_add_screen(self):
        sb.Popen(["Python", "_src/ui/add_card.py"])
        
    def Open_vizu_screen(self):
        sb.Popen(["python", "_src/ui/search_card.py"])
        
    def Open_edit_screen(self):
        sb.Popen(["Python", "_src/ui/view_card.py"])
        
    def Quit(self):
        self.master.destroy()
        

if __name__ == '__main__':
    screeen = ctk.CTk()
    screeen.title('Sistema de cartões digitais')
    app = Mainpage(screeen)
    
    screeen.geometry(f'{screeen.winfo_screenwidth()}x{screeen.winfo_screenheight()}')
    
    screeen.configure(fg_color = 'gray')
    screeen.mainloop()
