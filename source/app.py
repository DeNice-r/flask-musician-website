import sqlalchemy.exc
from flask import Flask, render_template
from dotenv import load_dotenv
import secrets
from os import getcwd, environ
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask("Maneskin website")
app.secret_key = secrets.token_hex()
app.config['DIR'] = getcwd()
# Heroku DB link
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2" + environ['DATABASE_URL'][8:]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['USER'] = 'Василь'
try:
    db = SQLAlchemy(app)
    db.create_all()
except sqlalchemy.exc.OperationalError:
    print("Cannot connect the database. Advancing without...")

# print(Accounts.query.all())

