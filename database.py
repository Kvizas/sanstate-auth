from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://auth-be@34.116.185.239/SS-Auth'
db = SQLAlchemy(app)
