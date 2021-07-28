from db_models.account import Account
from database import db
from flask import Blueprint

register_routes = Blueprint("register_routes", __name__)


@register_routes.route("/")
def register():
    db.session.add(Account(fname="Adam", lname="Roth"))
    db.session.commit()
    return "<p>Success</p>"
