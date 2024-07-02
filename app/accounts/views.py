import flask
from flask_login import current_user
from flask_login import login_required


from . import accounts

from ..models import db
from ..models import User


@accounts.route("/accounts/signin", methods=["GET", "POST"])
def sign_in():
    return flask.render_template("accounts/sign_in.html")

@accounts.route("/accounts/signup", methods=["GET", "POST"])
def sign_up():
    return flask.render_template("accounts/sign_up.html")
