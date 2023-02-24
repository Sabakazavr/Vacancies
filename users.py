import sqlite3
import asyncio
import logging

conn = sqlite3.connect('usersbase.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   user_id INT PRIMARY KEY,
   sub INT DEFAULT 0);
""")
conn.commit()

def get_all():
    cur.execute("SELECT * FROM users;")
    all_res = cur.fetchall()
    return all_res

def get_ids():
    cur.execute("SELECT user_id FROM users;")
    all_res = cur.fetchall()
    return all_res

def add_user(user):
    cur.execute("INSERT INTO users VALUES (?, ?)", [user, 0])
    conn.commit()

def get_sub(user):
    cur.execute("UPDATE users SET sub = 1 WHERE user_id = ?", [user])
    conn.commit()

def del_sub(user):
    cur.execute("UPDATE users SET sub = 0 WHERE user_id = ?", [user])
    conn.commit()

def find_user(user):
    cur.execute("SELECT user_id FROM users WHERE user_id = ?;", [user])
    for e in cur:
        if int(e[0]) == int(user):
            return True
    return False

