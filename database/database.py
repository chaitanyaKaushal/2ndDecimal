import sqlite3

conn = sqlite3.connect('decimal.db')

c = conn.cursor()

# c.execute(""" create table student(
#     id TEXT primary key,
#     roll_no TEXT,
#     name TEXT,
#     email TEXT,
#     sem TEXT,
#     year TEXT,
#     branch TEXT,
#     batch TEXT,
#     passwd TEXT
# )
# """)

# c.execute(""" create table teacher(
#     reg_id TEXT primary key,
#     name TEXT,
#     email TEXT,
#     subject TEXT,
#     passwd TEXT
# )
# """)

# c.execute(""" create table course(
#     id TEXT primary key,
#     course_name TEXT,
#     year TEXT,
#     branch TEXT,
#     sem TEXT
# )
# """)

# c.execute(""" create table announcement(
#     id TEXT primary key,
#     tid TEXT,
#     subject TEXT,
#     cid TEXT,
#     upper TEXT,
#     lower TEXT,
#     info TEXT
# )

# """)

# c.execute(""" create table schedule(
#     id TEXT primary key,
#     tid TEXT,
#     subject TEXT,
#     cid TEXT,
#     upper TEXT,
#     lower TEXT,
#     info TEXT
# )

# """)

# c.execute(""" create table cmaterial(
#     id TEXT primary key,
#     tid TEXT,
#     subject TEXT,
#     cid TEXT,
#     upper TEXT,
#     lower TEXT,
#     info TEXT
# )

# """)

# c.execute(""" create table staff(
#     id TEXT primary key,
#     name TEXT,
#     passwd TEXT,
#     email TEXT,
#     designation TEXT
# )

# """)

# c.execute(""" create table generalAnnouncement(
#     id TEXT primary key,
#     sid TEXT,
#     info TEXT,
#     year TEXT,
#     stream TEXT
# )

# """)

conn.commit()
conn.close()
