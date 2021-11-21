import datetime
from app import app, db
from flask import render_template, redirect, flash, request
from models.user import User
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from utils import is_url_safe


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Якщо користувач авторизований, не даємо йому авторизуватися це ще раз
    if current_user.is_authenticated:
        flash('Ви вже увійшли. Для зміни аккаунта потрібно спочатку вийти.', 'alert alert-info')
        return redirect('/')

    # Якщо метод пост
    if request.method == 'POST':
        # Запам'ятовуємо логін та пароль, після чого перевіряємо їх коректність
        user_login = request.form['login']
        user_password = request.form['password']

        if user_login and user_password:
            user = User.query.filter_by(username=user_login).first()
            if user is not None:
                # Якщо хеш наданого пароля підходить під хеш збереженого, то авторизуємо користувача
                if check_password_hash(user.password, user_password):
                    login_user(user)

                    # Та оновлюємо дату останнього входу
                    user.last_login = datetime.datetime.now()
                    db.session.commit()

                    # Отримуємо посилання для переходу далі
                    next_page = request.args.get('next')
                    # Якщо посилання безпечне, то переводимо на нього користувача, у іншому випадку переводимо його
                    # на головну
                    return redirect(next_page if is_url_safe(next_page) else '/')
            flash('Неправильний логін або пароль', 'alert alert-danger')
    # request.method == 'GET'
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    # Відкликаємо авторизацію користувача
    logout_user()
    return redirect('/')
