from flask_sqlalchemy import SQLAlchemy
from app import app

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://sql11433143@sql11.freesqldatabase.com/sql11433143"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
