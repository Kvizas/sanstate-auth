from db_models.account import Account
from database import db
from flask import Blueprint, request, jsonify, render_template
import assets.data_validation as dv
import bcrypt
from flask_cors import CORS
from functions.auth import get_jwt
from functions.register_functions import (
    send_registration_email,
    validate_registration_form,
)

register_routes = Blueprint("register_routes", __name__)
CORS(
    register_routes,
    origins=[
        "http://login.sanstate.lt",
        "https://login.sanstate.lt",
        "http://localhost:3000",
    ],
)


@register_routes.route("/", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"error": "Missing JSON body in request"}), 400

    try:
        data = request.json
        fname, lname, email, password = (
            data["fname"],
            data["lname"],
            data["email"],
            data["password"],
        )
    except KeyError:
        return jsonify({"error": "Visi laukeliai turi būti užpildyti"}), 400

    fname, lname = dv.fix_name_casing(fname), dv.fix_name_casing(lname)

    is_form_invalid = validate_registration_form(fname, lname, email, password)
    if is_form_invalid is not False:
        return (
            jsonify({"error": is_form_invalid.message, "field": is_form_invalid.field}),
            400,
        )

    name_check = db.session.query(Account).filter_by(fname=fname, lname=lname).count()
    if name_check > 0:
        return (
            jsonify(
                {
                    "error": "Paskyra su tokiu vardu bei pavarde jau egzistuoja",
                    "field": "name",
                }
            ),
            400,
        )

    email_check = db.session.query(Account).filter_by(email=email).count()
    if email_check > 0:
        return (
            jsonify(
                {
                    "error": "Paskyra su tokiu el. paštu jau užregistruota",
                    "field": "email",
                }
            ),
            400,
        )

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    acc = Account(
        fname=fname,
        lname=lname,
        email=email,
        password_hash=password_hash,
        activated=False,
    )

    db.session.add(acc)
    db.session.commit()

    send_registration_email(acc)
    return jsonify({"id": acc.id}), 200


@register_routes.route("/<int:userid>/<int:code>", methods=["POST"])
def email_confirmation(userid, code):

    user: Account = db.session.query(Account).filter_by(id=userid).first()
    if user is None:
        return jsonify({"error": "Klaidingas paskyros ID"}), 400

    if user.confirmation_code != code:
        return jsonify({"error": "Klaidingas autorizacijos kodas"}), 400

    user.confirmation_code = None
    user.activated = True
    db.session.commit()
    return jsonify({"success": True}), 200
