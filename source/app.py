import sqlalchemy.exc
from flask import Flask, render_template
from dotenv import load_dotenv
import secrets
from os import getcwd
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine

load_dotenv()

app = Flask("Maneskin website")
app.secret_key = secrets.token_hex()
app.config['DIR'] = getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:78de78@localhost/lab11base'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['USER'] = 'Василь'
try:
    db = SQLAlchemy(app)
    db.create_all()
except sqlalchemy.exc.OperationalError:
    print("Cannot connect the database. Advancing without...")

# print(Accounts.query.all())

