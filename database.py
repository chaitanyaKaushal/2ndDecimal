import sqlite3

conn = sqlite3.connect('decimal.db')

c = conn.cursor()

c.execute(""" create table student(
    id TEXT primary key,
    roll_no TEXT,
    name TEXT,
    email TEXT,
    sem TEXT,
    year TEXT,
    branch TEXT,
    batch TEXT,
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
    id TEXT primary key,
    course_name TEXT,
    year TEXT,
    branch TEXT,
    sem TEXT
)
""")

conn.commit()
conn.close()