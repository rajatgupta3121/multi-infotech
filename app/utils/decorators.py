from functools import wraps

from flask_login import current_user

from flask import redirect
from flask import url_for
from flask import flash


def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if current_user.role != "admin":

            flash(
                "Access denied.",
                "danger"
            )

            return redirect(
                url_for("main.home")
            )

        return f(*args, **kwargs)

    return decorated_function