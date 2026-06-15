from functools import wraps

from flask import abort
from flask_login import current_user, login_required


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(*args, **kwargs):
            if getattr(current_user, "role", None) not in roles:
                abort(403)
            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator
