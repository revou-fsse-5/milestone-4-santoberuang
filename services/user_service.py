from functools import wraps
from flask_login import current_user
from flask import redirect, url_for

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role == role:
                return f(*args, **kwargs)
            else:
                return redirect(url_for('display.unauthorized')), 403
        return wrapped
    return decorator

