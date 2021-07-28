from database import db


class Account(db.Model):
    __tablename__ = "Accounts"

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    email = db.Column(db.String(320))
    password = db.Column(db.String(60))
