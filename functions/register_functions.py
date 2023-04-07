import assets.data_validation as dv
from assets.data_validation import InvalidData
import sendgrid
import os
from random import randint
from db_models.account import Account
from flask import render_template
from datetime import date
from sendgrid.helpers.mail import *
from database import db


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
            confirmation_url=os.environ.get("SSLOGIN_API_URL") + "/register",
            year=date.today().year,
        ),
    )
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
