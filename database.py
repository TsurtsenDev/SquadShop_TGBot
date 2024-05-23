import sqlite3

def create_connection():
    conn = sqlite3.connect('bot_database.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            referrer_id INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY,
            referrer_id INTEGER,
            referred_user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(referrer_id) REFERENCES users(user_id),
            FOREIGN KEY(referred_user_id) REFERENCES users(user_id)
        )
    ''')

    conn.commit()
    conn.close()

def add_user(user_id, username, first_name, last_name, referrer_id=None):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, username, first_name, last_name, referrer_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name, referrer_id))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_referral(referrer_id, referred_user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO referrals (referrer_id, referred_user_id)
        VALUES (?, ?)
    ''', (referrer_id, referred_user_id))
    conn.commit()
    conn.close()


create_tables()
