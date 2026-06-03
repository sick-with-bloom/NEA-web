import sqlite3

def execute_query_one(query,params):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(query,params)
    row = cur.fetchone()
    return row

def execute_query_all(query,params):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(query,params)
    rows = cur.fetchall()
    return rows

def execute_query_add(query,params):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(query,params)
    conn.commit()