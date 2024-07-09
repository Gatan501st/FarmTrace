from functools import wraps
from app.models import User
from flask import redirect, url_for, abort
from flask_login import current_user

def email_verified(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not current_user.confirmed:
            return redirect(url_for('accounts.verify_email'))
        return f(*args, **kwargs)
    return decorator

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.role_title == role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator