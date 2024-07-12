from flask import Blueprint

listings = Blueprint('listings', __name__)

from . import views