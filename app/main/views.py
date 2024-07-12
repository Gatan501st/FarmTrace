import os
from datetime import datetime
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.main import main
from app.models.user import User
from app.email import send_confirmation_email, confirm_token


@main.route("/")
def index():
    return render_template("main/index.html")


@main.route("/about-us")
def about_us():
    return render_template("main/about_us.html")


@main.route("/how-it-works")
def how_it_works():
    return render_template("main/how_it_works.html")

@main.route("/contact-us")
def contact_us():
    return render_template("main/contact_us.html")
