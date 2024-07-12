from flask import Blueprint
from flask import current_app


accounts = Blueprint("accounts", __name__, url_prefix="/accounts")

from . import views
