from sendgrid.helpers.mail import email
from db_models.account import Account
from flask import Blueprint, request
from flask.json import jsonify
from database import db
from sqlalchemy import and_
import bcrypt

login_routes = Blueprint("login_routes", __name__)


@login_routes.route("/", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"error": "Missing JSON body in request"}), 400

    data = request.json
    identifier, password = (
        data["identifier"],
        data["password"],
    )

    splitted_identifier = identifier.split(" ")
    filter = (
        (Account.id == identifier) | (Account.email == identifier)
        if len(splitted_identifier) != 2
        else and_(
            Account.fname == splitted_identifier[0],
            Account.lname == splitted_identifier[1],
        )
    )

    user = db.session.query(Account).filter(filter).first()

    if user is None:
        return jsonify(
            {"error": "Paskyra tokiu vardu ir pavarde, el.paštu ar ID neegzistuoja"}
        )

    if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        return jsonify({"error": "Neteisingas slaptažodis"})

    return jsonify({}), 200
