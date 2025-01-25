import sqlite3

from sekret.key import DATABASE



def init_db():
    """Инициализация базы данных"""

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS whitelist (
            user_id INTEGER PRIMARY KEY
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            token TEXT PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()




def is_user_whitelisted(user_id):
    """Проверка белого списка"""

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM whitelist WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None




def add_user_to_whitelist(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Добавляем user_id в таблицу whitelist
    cursor.execute("INSERT OR IGNORE INTO whitelist (user_id) VALUES (?);", (user_id,))
    conn.commit()
    conn.close()
    print(f"User {user_id} добавлен в белый список.")




def add_token_to_database(token):
    """Добавление токена в таблицу tokens"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO tokens (token) VALUES (?)", (token,))
    conn.commit()
    conn.close()
    print(f"Токен {token} добавлен в базу данных.")



if __name__ == "__main__":
    """Добавляем Api и id админа"""
    from sekret.key import API_TOKEN_SANDBOX
    from sekret.key import API_TOKEN_LIVE
    from sekret.key import id_tg_admin

    # Добавьте токен в базу данных
    add_token_to_database(API_TOKEN_SANDBOX)
    add_token_to_database(API_TOKEN_LIVE)
    add_user_to_whitelist(id_tg_admin)