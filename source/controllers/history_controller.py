from app import app
from flask import render_template
from flask_login import current_user


@app.route('/history')
def history():
    return render_template('history.html', app=app, user=current_user)
