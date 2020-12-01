from flask import redirect, render_template, request, session, url_for
from functools import wraps


def loggedout(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uid") is not None:
            return redirect(url_for("logout"))
        return f(*args, **kwargs)
    return decorated_function


def loggedin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uid") is None:
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

def student_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uid") is None:
            return redirect("/")
        elif session.get("uid")[:2] != "su":
            return redirect(url_for("logout"))
        return f(*args, **kwargs)
    return decorated_function

def teacher_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uid") is None:
            return redirect("/")
        elif session.get("uid")[:2] != "te":
            return redirect(url_for("logout"))
        return f(*args, **kwargs)
    return decorated_function

def staff_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uid") is None:
            return redirect("/")
        elif session.get("uid")[:2] != "st":
            return redirect(url_for("logout"))
        return f(*args, **kwargs)
    return decorated_function