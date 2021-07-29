from app import app
from dotenv import load_dotenv

from routes.login import login_routes
from routes.register import register_routes

from database import db

db.create_all()
db.session.commit()

load_dotenv()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


app.register_blueprint(login_routes, url_prefix="/login")
app.register_blueprint(register_routes, url_prefix="/register")
