from flask import redirect, render_template, request, session
from functools import wraps


def loggedout(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uid") is not None:
            return redirect("/logout")
        return f(*args, **kwargs)
    return decorated_function


def loggedin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uid") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def student_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uid")[:3] != "su":
            return redirect("/logout")
        return f(*args, **kwargs)
    return decorated_function

def teacher_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uid")[:3] != "te":
            return redirect("/logout")
        return f(*args, **kwargs)
    return decorated_function

def staff_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uid")[:3] != "st":
            return redirect("/logout")
        return f(*args, **kwargs)
    return decorated_function