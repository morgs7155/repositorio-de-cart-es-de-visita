import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from PIL import Image, ImageTk


class VizuCard:
    def __init__(self, master):
        self.master = master
        self.db_file = "database/business_cards.db"
        self.Setup()

    def Setup(self):
        self.Frames()
        self.Labels()
        self.Entrys()
        self.Icons()
        self.Buttons()
        self.ListCards("")  #lista inicial sem filtros

    def db_execute(self, query, params=()):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()

    def Frames(self):
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()

        self.f_searchs = ctk.CTkFrame(self.master, width=self.width, height=100, fg_color='green')
        self.f_searchs.pack(side=tk.TOP)

        self.f_cards = ctk.CTkFrame(self.master, width=self.width, height=self.height - 100, fg_color='white')
        self.f_cards.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def Icons(self):
        self.icon_glass_open = Image.open('icons/glass.png')
        self.icon_glass_ofc = ctk.CTkImage(self.icon_glass_open, size=(30, 30))

    def Labels(self):
        self.l_search_name = ctk.CTkLabel(
            self.f_searchs, text='Nome/Empresa/E-mail:', font=('Times', 15, 'bold'), text_color='white'
        )
        self.l_search_name.place(x=10, y=30)

    def Entrys(self):
        self.e_search_card = ctk.CTkEntry(
            self.f_searchs, width=200, fg_color='white', border_color='green', placeholder_text='Digite para buscar'
        )
        self.e_search_card.place(x=200, y=30)

    def Buttons(self):
        self.btn_search_card = ctk.CTkButton(
            self.f_searchs,
            text='',
            image=self.icon_glass_ofc,
            font=('Times', 15, 'bold'),
            fg_color='green',
            width=50,
            hover_color='lightgreen',
            command=self.search_cards,
        )
        self.btn_search_card.place(x=410, y=25)

    def search_cards(self):
        query = self.e_search_card.get()
        self.ListCards(query)

    def ListCards(self, filter_text):
        """Lista de cartões"""
        for widget in self.f_cards.winfo_children():
            widget.destroy()

        query = "SELECT id, name, company, email FROM cards WHERE name LIKE ? OR company LIKE ? OR email LIKE ?"
        filter_param = f"%{filter_text}%"
        cards = self.db_execute(query, (filter_param, filter_param, filter_param))

        for i, (card_id, name, company, email) in enumerate(cards):
            btn_card = ctk.CTkButton(
                self.f_cards,
                text=f"{name} - {company} ({email})",
                command=lambda cid=card_id: self.show_card_details(cid),
                fg_color='grey',
                hover_color='lightblue',
            )
            btn_card.pack(pady=5, padx=10, fill=tk.X)

    def show_card_details(self, card_id):
        #exibe e permite edição dos detalhes do cartão
        details = self.db_execute("SELECT name, company, email, qrcode_path FROM cards WHERE id = ?", (card_id,))
        if not details:
            messagebox.showerror("Erro", "Cartão não encontrado.")
            return

        name, company, email, qr_path = details[0]
        details_window = ctk.CTkToplevel(self.master)
        details_window.geometry('500x600')
        details_window.title(f"Detalhes: {name}")

        ctk.CTkLabel(details_window, text="Editar Dados do Cartão", font=("Arial", 18, "bold")).pack(pady=10)

        #campos editáveis
        ctk.CTkLabel(details_window, text="Nome:").pack(pady=5)
        entry_name = ctk.CTkEntry(details_window, width=300, fg_color='white')
        entry_name.insert(0, name)
        entry_name.pack(pady=5)

        ctk.CTkLabel(details_window, text="Empresa:").pack(pady=5)
        entry_company = ctk.CTkEntry(details_window, width=300, fg_color='white')
        entry_company.insert(0, company)
        entry_company.pack(pady=5)

        ctk.CTkLabel(details_window, text="E-mail:").pack(pady=5)
        entry_email = ctk.CTkEntry(details_window, width=300, fg_color='white')
        entry_email.insert(0, email)
        entry_email.pack(pady=5)

        #exibi o QR Code
        if os.path.exists(qr_path):
            qr_image = Image.open(qr_path)
            qr_photo = ctk.CTkImage(qr_image, size=(200, 200))
            label_qr = ctk.CTkLabel(details_window, image=qr_photo, text="")
            label_qr.image = qr_photo
            label_qr.pack(pady=10)

        def save_changes():
            new_name = entry_name.get().strip()
            new_company = entry_company.get().strip()
            new_email = entry_email.get().strip()

            if not new_name or not new_email:
                messagebox.showerror("Erro", "Os campos Nome e E-mail são obrigatórios.")
                return

            try:
                self.db_execute(
                    "UPDATE cards SET name = ?, company = ?, email = ? WHERE id = ?",
                    (new_name, new_company, new_email, card_id),
                )
                messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                details_window.destroy()
                self.ListCards("")  #atualiza a lista
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível atualizar os dados: {e}")

        ctk.CTkButton(
            details_window,
            text="Salvar Alterações",
            fg_color="blue",
            hover_color="darkblue",
            command=save_changes,
        ).pack(pady=10)

        ctk.CTkButton(
            details_window,
            text="Excluir",
            fg_color="red",
            hover_color="darkred",
            command=lambda: self.delete_card(card_id, qr_path, details_window),
        ).pack(pady=10)

    def delete_card(self, card_id, qr_path, window):
        """deleta o cartão do banco de dados"""
        try:
            self.db_execute("DELETE FROM cards WHERE id = ?", (card_id,))
            if os.path.exists(qr_path):
                os.remove(qr_path)
            messagebox.showinfo("Sucesso", "Cartão removido com sucesso!")
            window.destroy()
            self.ListCards("")  #atualiza lista
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível remover o cartão: {e}")


if __name__ == "__main__":
    screen = ctk.CTk()
    screen.title('Visualizar e Editar Cartões de Visita')
    app = VizuCard(screen)
    screen.geometry(f"{screen.winfo_screenwidth()}x{screen.winfo_screenheight()}")
    screen.mainloop()
