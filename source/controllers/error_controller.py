from flask import Flask, render_template
from app import app


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', app=app), 404
