import sqlite3
import hashlib
try: 
    import colorama
    colorama.init(autoreset=True)
    print(f"{colorama.Fore.LIGHTGREEN_EX}+====================+\n\n{colorama.Fore.GREEN}Database Utils Loaded!{colorama.Fore.RESET}\n\n{colorama.Fore.LIGHTGREEN_EX}+====================+")
except ImportError:
    print("+====================+\n\nDatabase Utils Loaded!\n\n+====================+")
conn = sqlite3.connect('userdata.db', check_same_thread=False)
cur = conn.cursor()

def init_database():
    cur.execute('''
                CREATE TABLE IF NOT EXISTS accounts(username text, password text)
                ''')

def get_by_username(username):
    cur.execute("SELECT * FROM accounts WHERE username = ?", (username,))
    return cur.fetchone()    

def create_account(username: str, password: str):
    password = hashlib.sha256(password.encode()).hexdigest()
    
    if get_by_username(username) != None:
        return 1
    cur.execute("INSERT INTO accounts VALUES (?,?)", (username, password))
    conn.commit()
    return 0

init_database()
