from app import app
from flask import render_template
from flask_login import current_user


@app.route('/about')
def about():
    return render_template('about.html')
