from cs50 import SQL
import csv
from werkzeug.security import check_password_hash, generate_password_hash

db = SQL("sqlite:///decimal.db")

def regStudent(file):
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            db.execute("""Insert into student(id, roll_no, name, email, sem, year, branch, batch, passwd) 
                        values(:id, :roll, :name, :email, :sem, :year, :branch, :batch, :passw)""", 
                        id = row["id"], roll = row["roll_no"], name = row["name"], email = row["email"], sem = row["semester"], year = row["year"]
                        , branch = row["branch"], batch = row["batch"], passw = generate_password_hash(row["passwd"]))

def regTeacher(file):
    
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            db.esqplite3xecute("""Insert into teacher(reg_id, name, email, subject, passwd) 
                        values(:id, :name, :email, :subject, :passwd)""", 
                        id = row["reg_id"], name = row["name"], email = row["email"],
                        subject = row["subject"], passwd = generate_password_hash(row["passwd"]))

def regCourse(file):
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            db.execute("""Insert into course(course_name, year, branch, sem) 
                        values(:course_name, :year, :branch, :sem)""", 
                        course_name = row["course_name"], year = row["year"], branch = row["branch"], sem = row["sem"]
                        )

# regCourse("./course.csv")
# regTeacher("./teacher.csv")
# regStudent("./teacher.csv")