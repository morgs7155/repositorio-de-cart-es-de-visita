import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image
import requests
import os

class AddCard:
    def __init__(self, master):
        self.master = master
        self.Setup()
    
    def Setup(self):
        self.Frames()
        self.Labels()
        self.Entrys()
        self.Icons()
        self.Buttons()
        
    def Frames(self):
        self.f_add_datared = ctk.CTkFrame(self.master, width=500, height=500, fg_color='white')
        self.f_add_datared.pack(side=tk.TOP, expand=True)
        
    def Icons(self):
        self.icon_help_open = Image.open('icons/help.png')
        self.icon_help_resize = self.icon_help_open.resize((50, 50), Image.Resampling.LANCZOS)
        self.icon_help_ofc = ctk.CTkImage(self.icon_help_resize, size=(30, 30))
        
    def Labels(self):
        labels = ['Nome:', 'Empresa:', 'Cargo:', 'Email:', 'Telefone:', 'Endereço:', 'Site:']
        for idx, text in enumerate(labels):
            label = ctk.CTkLabel(self.f_add_datared, text=text, font=('Times', 15, 'bold'))
            label.place(x=10, y=50 + idx*50)
        
    def Entrys(self):
        self.entries = {
            'nome': ctk.CTkEntry(self.f_add_datared, width=300, font=('Times', 15, 'bold'), placeholder_text='Digite um nome para o cartão'),
            'empresa': ctk.CTkEntry(self.f_add_datared, width=300, font=('Times', 15, 'bold'), placeholder_text='Digite o nome da empresa'),
            'cargo': ctk.CTkEntry(self.f_add_datared, width=300, font=('Times', 15, 'bold'), placeholder_text='Digite o seu cargo'),
            'email': ctk.CTkEntry(self.f_add_datared, width=300, font=('Times', 15, 'bold'), placeholder_text='Digite o email'),
            'telefone': ctk.CTkEntry(self.f_add_datared, width=300, font=('Times', 15, 'bold'), placeholder_text='Digite o número de telefone'),
            'endereco': ctk.CTkEntry(self.f_add_datared, width=300, font=('Times', 15, 'bold'), placeholder_text='Digite o endereço'),
            'site': ctk.CTkEntry(self.f_add_datared, width=300, font=('Times', 15, 'bold'), placeholder_text='Digite a URL do site'),
        }
        for idx, entry in enumerate(self.entries.values()):
            entry.place(x=100, y=50 + idx*50)
        
    def Buttons(self):
        self.btn_insert_card = ctk.CTkButton(self.f_add_datared, text='Salvar', font=('Times', 15, 'bold'),
                                             fg_color='red', hover_color='#FD8F90', text_color='white', 
                                             command=self.check_and_save_card)
        self.btn_insert_card.place(x=170, y=400)
        
        self.btn_help = ctk.CTkButton(self.f_add_datared, text='', image=self.icon_help_ofc, fg_color='white', 
                                      hover_color="#f4f4f4", text_color='black', width=30)
        self.btn_help.place(x=440, y=0)
        
    def create_qr_code(self):
        data = f"Nome: {self.entries['nome'].get()}, Empresa: {self.entries['empresa'].get()}, Cargo: {self.entries['cargo'].get()}, Email: {self.entries['email'].get()}, Telefone: {self.entries['telefone'].get()}, Endereço: {self.entries['endereco'].get()}, Site: {self.entries['site'].get()}"
        
        url_api = f'https://api.qrserver.com/v1/create-qr-code/?data={data}&size=200x200'
        response = requests.get(url_api)
        
        if response.status_code == 200: 
            #especificando caminho onde o qr code sera salvo
            output_dir = "assets/qr_codes"
            os.makedirs(output_dir, exist_ok=True)
        
            #salvando qr code como png
            file_path = os.path.join(output_dir, f"{self.entries['nome'].get()}.png")
            with open(file_path, "wb") as file:
                file.write(response.content)
            messagebox.showinfo(f"Cartão virtual gerado e salco", f'Verifique seu novo cartão na sua pagina de cartões salvos')
            return file_path
        else:
            messagebox.showerror(f"Erro ao gerar o QR Code", f"erro: {response.status_code}")
            return None

    def check_and_save_card(self):
        email = self.entries['email'].get()
        try:
            conn = sqlite3.connect("database/business_cards.db")
            cursor = conn.cursor()
            
            #verificação de duplicidade de email
            cursor.execute("SELECT * FROM cards WHERE email = ?", (email,))
            if cursor.fetchone():
                messagebox.showwarning("Duplicata encontrada", "Um cartão com esse e-mail já existe.")
                conn.close()
                return
            
            #gerando qr code
            qrcode_path = self.create_qr_code()
            if qrcode_path is None:
                messagebox.showerror("Erro", "Falha ao gerar o QR Code.")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO cards (name, company, position, email, phone, address, website, qrcode_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.entries['nome'].get().upper(), self.entries['empresa'].get().upper(), self.entries['cargo'].get().upper(),
                  email, self.entries['telefone'].get(), self.entries['endereco'].get().upper(),
                  self.entries['site'].get(), qrcode_path))
            
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Cartão '{self.entries['nome'].get()}' adicionado com sucesso.")
        
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", f"Erro: {e}")
        

if __name__ == '__main__':
    screeen = ctk.CTk()
    screeen.title('Adicionar Cartão Digital')
    screeen.resizable(width=False, height=False)
    app = AddCard(screeen)
    
    screeen.geometry('500x500')
    screeen.mainloop()
