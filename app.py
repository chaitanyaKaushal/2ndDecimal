from flask import Flask, flash, jsonify, redirect, render_template, request, session, Markup
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from cs50 import SQL
from helper import staff_login, student_login, teacher_login

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
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    details = db.execute("select * from student where id = :id", id = session["uid"])
    return render_template("home.html", name = details[0]["name"], batch = details[0]["batch"], id = details[0]["roll_no"])

@app.route("/studentlogin", methods = ["GET", "POST"])
def studentlogin():
    if request.method == "GET":
        return render_template("studentlogin.html")
    else:
        name = request.form.get("uname")
        passw = request.form.get("pass")
        apass = db.execute("Select * from student where roll_no = :roll", roll = name)
        if len(apass) == 0:
            return render_template("studentlogin.html", error = "User doesnot exist")
        if not check_password_hash(apass[0]["passwd"], passw):
            return render_template("studentlogin.html", error = "Invalid details")
        session["uid"] = apass[0]["id"]
        return redirect("/home")
        
@app.route("/teacherlogin")
def teacherlogin():
    return render_template("teacherlogin.html")

@app.route("/stafflogin")
def stafflogin():
    return render_template("stafflogin.html")