import os

import json
import flask

from . import main


@main.route("/")
@main.route("/home")
@main.route("/homepage")
def index():
    return flask.render_template("main/index.html")


@main.route("/about-us")
def about_us():
    return flask.render_template("main/about_us.html")


@main.route("/how-it-works")
def how_it_works():
    return flask.render_template("main/how_it_works.html")


@main.route("/contact-us")
def contact_us():
    return flask.render_template("main/contact_us.html")
