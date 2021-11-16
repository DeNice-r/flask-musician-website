import datetime

from app import app, db
from flask import render_template, redirect, flash, request
from models.user import User
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from utils import is_url_safe


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Ви вже увійшли. Для зміни аккаунта потрібно спочатку вийти.', 'alert alert-info')
        return redirect('/')

    if request.method == 'POST':
        user_login = request.form['login']
        user_password = request.form['password']

        if user_login and user_password:
            user = User.query.filter_by(username=user_login).first()
            if user is not None:
                if check_password_hash(user.password, user_password):
                    login_user(user)

                    user.last_login = datetime.datetime.now()
                    db.session.commit()

                    next_page = request.args.get('next')

                    # Если ссылка безопасна, переводим на неё пользователя, иначе переводим его на главную
                    return redirect(next_page if is_url_safe(next_page) else '/')
            flash('Неправильний логін або пароль', 'alert alert-danger')
    # request.method == 'GET'
    return render_template("login.html", app=app, user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
