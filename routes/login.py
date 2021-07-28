from flask import Blueprint

login_routes = Blueprint("login_routes", __name__)


@login_routes.route("/")
def login():
    return "<p>%s</p>".format()
