from flask import Flask, render_template
from app import app


@app.route('/history')
def history():
    return render_template('history.html', app=app)
