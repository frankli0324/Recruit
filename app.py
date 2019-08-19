import os

from flask import Flask

from api import challenge, user
from models import db
from view import view

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') or \
                                        'mysql+pymysql://username:password@localhost/judge?charset=utf8mb4'
with app.app_context():
    db.init_app(app)
    db.create_all()

app.register_blueprint(challenge)
app.register_blueprint(user)
app.register_blueprint(view)
