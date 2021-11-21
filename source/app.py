from flask import Flask
from dotenv import load_dotenv
from os import getcwd, environ
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy


# Завантажуємо змінні середовища
load_dotenv()

app = Flask("Maneskin website")

# Секретний ключ (потрібен, наприклад, щоб отримувати POST-запити)
app.secret_key = environ['SECRET_KEY']

# Папка, у якій працює програма
app.config['DIR'] = getcwd()

# Режим відладки
app.config['DEBUG'] = eval(environ['DEBUG'])

# Прийнятні розширення картинок
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PICTURE_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']

# Конфігурація підключення до бд
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2" + environ['DATABASE_URL'][8:]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Створення підключення до бд
db = SQLAlchemy(app)

# Створення менеджера авторизації
lm = LoginManager(app)

# Конфігурація менеджера авторизації
lm.login_view = '/login'
lm.login_message = 'Ця сторінка доступна лише авторизованим користувачам.'
lm.login_message_category = 'alert alert-danger'


# Додання контексту у темплейти
@app.context_processor
def inject_app():
    return {'app': app}


@app.context_processor
def inject_user():
    return {'user': current_user}
