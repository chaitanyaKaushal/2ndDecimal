import sqlite3

conn = sqlite3.connect('decimal.db')

c = conn.cursor()

c.execute(""" create table student(
    reg_id TEXT primary key,
    roll_no TEXT,
    name TEXT,
    email TEXT,
    semester TEXT,
    year TEXT,
    branch TEXT,
    batch TEXT,
    course TEXT,
    passwd TEXT
)

""")

c.execute(""" create table teacher(
    reg_id TEXT primary key,
    name TEXT,
    email TEXT,
    subject TEXT,
    passwd TEXT
)

""")

c.execute(""" create table course(
    course_name TEXT,
    year TEXT,
    branch TEXT,
    batch TEXT
)

""")

conn.commit()
conn.close()