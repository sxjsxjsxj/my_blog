from flask import session, render_template
from functools import wraps


def login_required(func):
    @wraps(func)
    def check(*args,**kwargs):
        try:
            if not session['id']:
                return func(*args,**kwargs)
        except:
            return render_template('back/login.html')
    return check

def login_required1(func):
    @wraps(func)
    def check(*args,**kwargs):
        try:
            if not session['id']:
                return func(*args,**kwargs)
        except:
            return render_template('web/login_index.html')
    return check