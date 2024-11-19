import sqlite3

class Database():
    def __init__(self):
        self.Data_cards()
        
    def Data_cards(self):
        self.conn = sqlite3.connect("database/business_cards.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS cards(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            website TEXT NOT NULL,
            qrcode_path TEXT NOT NULL,
            creat_at DATETIME
        )""")
        
        self.conn.commit()
        self.conn.close()
    
if __name__ == '__main__':
    Database()