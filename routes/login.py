from sendgrid.helpers.mail import email
from db_models.account import Account
from flask import Blueprint, request
from flask.json import jsonify
from database import db
from sqlalchemy import and_
import bcrypt
from flask_cors import CORS
from functions.auth import get_jwt

login_routes = Blueprint("login_routes", __name__)
CORS(login_routes)


@login_routes.route("/", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"error": "Missing JSON body in request"}), 400

    data = request.json

    try:
        identifier, password = (
            data["identifier"],
            data["password"],
        )
    except KeyError:
        return jsonify({"error": "Visi laukeliai turi būti užpildyti"}), 400

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
        return (
            jsonify(
                {
                    "error": "Paskyra neegzistuoja",
                    "field": "identifier",
                }
            ),
            400,
        )

    if user.activated is False:
        return (
            jsonify(
                {
                    "error": "Paskyra neaktyvuota (patikrinkite el. paštą)",
                    "field": "identifier",
                }
            ),
            400,
        )

    if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        return jsonify({"error": "Neteisingas slaptažodis", "field": "password"}), 400

    return jsonify({"jwt": get_jwt(user)}), 200
