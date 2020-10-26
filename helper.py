from flask import redirect, render_template, request, session
from functools import wraps

def student_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id")[:3] != "su":
            return redirect("/studentlogin")
        return f(*args, **kwargs)
    return decorated_function

def teacher_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id")[:3] != "te":
            return redirect("/teacherlogin")
        return f(*args, **kwargs)
    return decorated_function

def staff_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id")[:3] != "st":
            return redirect("/stafflogin")
        return f(*args, **kwargs)
    return decorated_function