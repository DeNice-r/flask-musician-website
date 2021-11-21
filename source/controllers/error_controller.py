from app import app
from flask import render_template
from flask_login import current_user


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


@app.errorhandler(401)
def not_authorized(error):
    return render_template('error.html'), 401

