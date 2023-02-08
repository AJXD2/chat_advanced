import sqlite3

conn = sqlite3.connect('userdata.db')
cur = conn.cursor()
def init_database():
    cur.execute('''
                CREATE TABLE IF NOT EXISTS accounts(id primary key, username text, password text)
                ''')

def get_by_username(username):
    cur.execute('''SELECT * FROM accounts WHERE username = ?''', (username,))
    return cur.fetchone()    

def create_account(username):
    cur.execute('''SELECT * FROM accounts WHERE username = ?''', (username,))
    return cur.fetchone()        

print(get_by_username('AJXD2'))