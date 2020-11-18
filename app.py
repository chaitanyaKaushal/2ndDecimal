from flask import Flask, flash, jsonify, redirect, render_template, request, session, Markup
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from cs50 import SQL
from helper import staff_login, student_login, teacher_login, loggedin, loggedout

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.debug = True

db = SQL("sqlite:///./database/decimal.db")

@app.route("/")
@loggedout
def index():
    return render_template("index.html")
    
@app.route("/studentlogin", methods = ["GET", "POST"])
@loggedout
def studentlogin():
    if request.method == "GET":
        return render_template("studentlogin.html")
    else:
        name = request.form.get("uname")
        passw = request.form.get("pass")
        apass = db.execute("Select * from student where roll_no = :roll", roll = name)
        if len(apass) == 0:
            return render_template("studentlogin.html", error = "User does not exist")
        if not check_password_hash(apass[0]["passwd"], passw):
            return render_template("studentlogin.html", error = "Invalid details")
        session["uid"] = apass[0]["id"]
        return redirect("/home")

@app.route("/teacherlogin", methods = ["GET", "POST"])
@loggedout
def teacherlogin():
    if request.method == "GET":
        return render_template("teacherlogin.html")
    else:
        email = request.form.get("uname")
        passw = request.form.get("pass")
        apass = db.execute("select * from teacher where email = :em",em = email)
        if len(apass) == 0:
            return render_template("teacherlogin.html",error = "User does not exist" )
        if not check_password_hash(apass[0]["passwd"],passw) :
            return render_template("teacherlogin.html",error = "Invalid details")
        session["uid"] = apass[0]["reg_id"]
        return redirect("/home")

@app.route("/stafflogin", methods = ["POST", "GET"])
@loggedout
def stafflogin():
    if request.method == "GET":
        return render_template("stafflogin.html")
    else:
        email = request.form.get("uname")
        passw = request.form.get("pass")
        apass = db.execute("select * from staff where email = :em",em = email)
        if len(apass) == 0:
            return render_template("teacherlogin.html",error = "User does not exist" )
        if not check_password_hash(apass[0]["passwd"],passw) :
            return render_template("teacherlogin.html",error = "Invalid details")
        session["uid"] = apass[0]["id"]
        return redirect("/staffhome")

@app.route("/home")
@loggedin
def home():
    if session["uid"][:2] == "su": 
        details = db.execute("select * from student where id = :id", id = session["uid"])
        courses = db.execute("select course_name, id from course where branch = :branch and sem = :sem", branch = details[0]["branch"], sem = details[0]["sem"])
        return render_template("student_page.html", sid = session["uid"], id = session["uid"][:2], courses = courses, name = details[0]["name"])
    elif session["uid"][:2] == "te":
        details = db.execute("select * from teacher where reg_id = :id", id = session["uid"])
        subcode = details[0]["subject"].split(',')
        subjects = []
        for code in subcode:
            temp = db.execute("select id, course_name from course where id = :id", id = code)
            print(temp)
            subjects.append(temp[0])
        return render_template("student_page.html", sid = session["uid"], id = session["uid"][:2], courses = subjects, name = details[0]["name"])

@app.route("/staffhome")
@staff_login
def staffhome():
    return render_template("staffhome.html")

@app.route("/course")
@loggedin
def course():
    sid = request.args.get("id")
    course = db.execute("select * from course where id = :sid", sid = sid)
    course = course[0]
    name = ""
    uid = session["uid"]
    if session["uid"][:2] == "su":
        student = db.execute("select * from student where id = :uid", uid = uid)
        student = student[0]
        name = student["name"]
        cmaterials = db.execute("select * from cmaterial where cid = :cid and :batch >= lower and :batch <= upper", cid = sid, batch = int(student["batch"]))
        announcements = db.execute("select * from announcement where cid = :cid and :batch >= lower and :batch <= upper", cid = sid, batch = int(student["batch"]))
        schedules = db.execute("select * from schedule where cid = :cid and :batch >= lower and :batch <= upper", cid = sid, batch = int(student["batch"]))
        return render_template("course.html", course_name = course["course_name"], id = session["uid"][:2], name = name, cmaterials = cmaterials, announcements = announcements, schedules = schedules)
    else:
        teacher = db.execute("select * from teacher where reg_id = :uid", uid = uid)
        teacher = teacher[0]
        name = teacher["name"]
        cmaterials = db.execute("select * from cmaterial where cid = :cid and tid = :tid", cid = sid, tid = session["uid"])
        announcements = db.execute("select * from announcement where cid = :cid and tid = :tid", cid = sid, tid = session["uid"])
        schedules = db.execute("select * from schedule where cid = :cid and tid = :tid", cid = sid, tid = session["uid"])
        return render_template("course.html", course_name = course["course_name"], id = session["uid"][:2], name = name, cmaterials = cmaterials, announcements = announcements, schedules = schedules)


@app.route("/logout", methods = ["GET", "POST"])
@loggedin
def logout():
    if request.method == "GET":
        return render_template("logout.html")
    else:
        session.clear()
        return redirect("/")
    
@app.route("/logout2")
@loggedin
def logout2():
    session.clear()
    return redirect("/")

@app.route("/delannounce", methods = ["GET", "POST"])
@teacher_login
def delannounce():
    if request.method == "POST":
        aid = request.args.get("id")
        db.execute("delete from announcement where id= :id", id = aid)
        return redirect("/home")
    
@app.route("/delschedule", methods = ["GET", "POST"])
@teacher_login
def delschedule():
    if request.method == "POST":
        aid = request.args.get("id")
        db.execute("delete from schedule where id= :id", id = aid)
        return redirect("/home")
    
@app.route("/delmaterial", methods = ["GET", "POST"])
@teacher_login
def delmaterial():
    if request.method == "POST":
        aid = request.args.get("id")
        db.execute("delete from cmaterial where id= :id", id = aid)
        return redirect("/home")

@app.route("/cannouncements", methods = ["GET", "POST"])
@teacher_login
def cannouncemennts():
    if request.method == "GET":
        teacher = db.execute("select * from teacher where reg_id = :id", id = session["uid"])
        teacher = teacher[0]
        temp = teacher["subject"].split(",")
        subjects = []
        for i in temp:
            sub = db.execute("select * from course where id = :id", id = i)
            subjects.append([sub[0], i])
        #print(subjects)
        #print(teacher)
        return render_template("cannouncements.html", subjects = subjects, name = teacher["name"])
    else:
        subject = request.form.get("subject")
        text = request.form.get("text")
        lower = request.form.get("lower")
        upper = request.form.get("upper")
        subs = db.execute("select subject from teacher where reg_id = :id", id = session["uid"])
        subject = subject.split(" ")
        cid = subject[-1]
        name= ""
        for i in range(len(subject) - 1):
            name += subject[i]
        db.execute("insert into announcement(tid, subject, cid, upper, lower, info) values(:tid, :sub, :cid, :upper, :lower, :info)", tid = session["uid"], sub = name, cid= cid, upper = upper, lower = lower, info = text)
        return redirect("/home")


@app.route("/schedule", methods = ["GET", "POST"])
@teacher_login
def schedule():
    if request.method == "GET":
        teacher = db.execute("select * from teacher where reg_id = :id", id = session["uid"])
        teacher = teacher[0]
        temp = teacher["subject"].split(",")
        print(temp)
        subjects = []
        for i in temp:
            sub = db.execute("select * from course where id = :id", id = i)
            subjects.append([sub[0], i])
        #print(subjects)
        print(teacher)
        return render_template("schedule.html", subjects = subjects, name = teacher["name"])
    else:
        subject = request.form.get("subject")
        text = request.form.get("text")
        lower = request.form.get("lower")
        upper = request.form.get("upper")
        subs = db.execute("select subject from teacher where reg_id = :id", id = session["uid"])
        subject = subject.split(" ")
        print(subject)
        cid = subject[-1]
        name= ""
        for i in range(len(subject) - 1):
            name += subject[i]
        db.execute("insert into schedule(tid, subject, cid, upper, lower, info) values(:tid, :sub, :cid, :upper, :lower, :info)", tid = session["uid"], sub = name, cid= cid, upper = upper, lower = lower, info = text)
        return redirect("/home")

@app.route("/cmaterial", methods = ["GET", "POST"])
@teacher_login
def cmaterial():
    if request.method == "GET":
        teacher = db.execute("select * from teacher where reg_id = :id", id = session["uid"])
        teacher = teacher[0]
        temp = teacher["subject"].split(",")
        subjects = []
        for i in temp:
            sub = db.execute("select * from course where id = :id", id = i)
            subjects.append([sub[0], i])
        #print(subjects)
        #print(teacher)
        return render_template("cmaterial.html", subjects = subjects, name = teacher["name"])
    else:
        subject = request.form.get("subject")
        text = request.form.get("text")
        lower = request.form.get("lower")
        upper = request.form.get("upper")
        subs = db.execute("select subject from teacher where reg_id = :id", id = session["uid"])
        subject = subject.split(" ")
        cid = subject[-1]
        name= ""
        for i in range(len(subject) - 1):
            name += subject[i]
        db.execute("insert into cmaterial(tid, subject, cid, upper, lower, info) values(:tid, :sub, :cid, :upper, :lower, :info)", tid = session["uid"], sub = name, cid= cid, upper = upper, lower = lower, info = text)
        return redirect("/home")

@app.route("/gannouncement", methods = ["GET", "POST"])
@staff_login
def gannouncement():
    if request.method == "GET":
        return render_template("staff_form.html")
