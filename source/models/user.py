from app import db, lm
from flask_login import UserMixin


# Створюємо модель користувача
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)


# Надаємо можливість завантажувати користувача менеджеру авторизації
@lm.user_loader
def user_loader(user_id):
    return User.query.get(user_id)
