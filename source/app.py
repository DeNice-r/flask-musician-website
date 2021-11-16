import datetime

from flask import Flask
from dotenv import load_dotenv
from os import getcwd, environ
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# Load environment variables
load_dotenv()

app = Flask("Maneskin website")

# Secret key (e.g. to receive post requests)
app.secret_key = environ['SECRET_KEY']

# Current working directory
app.config['DIR'] = getcwd()

# Режим відладки
app.config['DEBUG'] = eval(environ['DEBUG'])

# Allowed image extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PICTURE_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']

# App DB configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2" + environ['DATABASE_URL'][8:]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# DB connection creation
db = SQLAlchemy(app)

# Login manager creation
lm = LoginManager(app)

# Login manager configuration
lm.login_view = '/login'
lm.login_message = 'Ця сторінка доступна лише авторизованим користувачам.'
lm.login_message_category = 'alert alert-danger'

# Notes
# app.config['USER'] = 'Василь'
# print(Accounts.query.all())


# Add new user
# from models.user import User
# if len(User.query.all()) == 0:
#     print('11231233333333333333333333333')
#     from werkzeug.security import generate_password_hash
#     u = User(username='admin', password=generate_password_hash('password'), last_login=datetime.datetime.now())
#     db.session.add(u)
#     db.session.commit()
