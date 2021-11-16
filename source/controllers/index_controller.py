from app import app
from flask import render_template
from flask_login import current_user


@app.route('/')
def index():
    return render_template("index.html", app=app, user=current_user)
