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

db = SQL("sqlite:///decimal.db")

@app.route("/")
@loggedout
def index():
    return render_template("index.html")

@app.route("/home")
@loggedin
def home():
    if session["uid"][:2] == "su": 
        details = db.execute("select * from student where id = :id", id = session["uid"])
        courses = db.execute("select course_name from course where branch = :branch and sem = :sem", branch = details[0]["branch"], sem = details[0]["sem"])
        print(courses)
        return render_template("student_page.html", sid = session["uid"], id = session["uid"][:2], courses = courses, name = details[0]["name"])
    elif session["uid"][:2] == "te":
        details = db.execute("select * from teacher where reg_id = :id", id = session["uid"])
        subjects = details[0]["subject"].split(',')
        return render_template("student_page.html", sid = session["uid"], id = session["uid"][:2], courses = subjects, name = details[0]["name"])
    
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
        print(email)
        passw = request.form.get("pass")
        apass = db.execute("select * from teacher where email = :em",em = email)
        if len(apass) == 0:
            return render_template("teacherlogin.html",error = "User does not exist" )
        if not check_password_hash(apass[0]["passwd"],passw) :
            return render_template("teacherlogin.html",error = "Invalid details")
        print(apass[0]["reg_id"])
        session["uid"] = apass[0]["reg_id"]
        return redirect("/home")

@app.route("/stafflogin")
@loggedout
def stafflogin():
    return render_template("stafflogin.html")

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