from datetime import date
from db_models.account import Account
from database import db
from flask import Blueprint, request, jsonify, render_template
import assets.data_validation as dv
from assets.data_validation import InvalidData
import sendgrid
from sendgrid.helpers.mail import *
import bcrypt
import os
from random import randint

register_routes = Blueprint("register_routes", __name__)


@register_routes.route("/", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"error": "Missing JSON body in request"}), 400

    data = request.json
    fname, lname, email, password = (
        data["fname"],
        data["lname"],
        data["email"],
        data["password"],
    )

    fname, lname = dv.fix_name_casing(fname), dv.fix_name_casing(lname)

    is_form_invalid = validate_registration_form(fname, lname, email, password)
    if is_form_invalid is not False:
        return jsonify({"error": is_form_invalid.message}), 400

    name_check = db.session.query(Account).filter_by(fname=fname, lname=lname).count()
    if name_check > 0:
        return (
            jsonify({"error": "Paskyra su tokiu vardu bei pavarde jau egzistuoja"}),
            400,
        )

    email_check = db.session.query(Account).filter_by(email=email).count()
    if email_check > 0:
        return jsonify({"error": "Paskyra su tokiu el. paštu jau užregistruota"}), 400

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
    return "<p>Success</p>"


def validate_registration_form(fname, lname, email, password):

    fname_check = dv.validate_name(fname)
    lname_check = dv.validate_name(lname)
    email_check = dv.validate_email(email)
    password_check = dv.validate_password(password)

    return next(
        (
            x
            for x in [fname_check, lname_check, email_check, password_check]
            if isinstance(x, InvalidData)
        ),
        False,
    )


def send_registration_email(acc: Account):

    acc.confirmation_code = randint(1000, 9999)
    db.session.commit()

    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
    from_email = Email(email=os.environ.get("SYSTEM_EMAIL"), name="sanstate.lt Sistema")
    to_email = To(acc.email)
    subject = "Registracijos patvirtinimas"
    content = Content(
        "text/html",
        render_template(
            "register.html",
            name=acc.fname.upper() + " " + acc.lname.upper(),
            id=acc.id,
            code=acc.confirmation_code,
            confirmation_url=os.environ.get("API_URL") + "/register",
            year=date.today().year,
        ),
    )
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())


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
