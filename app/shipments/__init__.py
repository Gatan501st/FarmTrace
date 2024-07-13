from flask import Blueprint

shipments = Blueprint('shipments', __name__)

from . import views
