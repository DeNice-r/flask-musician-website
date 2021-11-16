from app import app
from flask import request, flash
from secrets import token_urlsafe
from urllib.parse import urlparse, urljoin
import os


def is_picture(filename: str):
    if '.' in filename:
        split = filename.rsplit('.', 1)
        if len(split) == 2:
            return split[1].lower() in app.config['PICTURE_EXTENSIONS']
    return False


def secure_save_image(image):
    # если картинка подходит
    if is_picture(image.filename):
        # то загружаем её
        # Для начала получаем расширение
        ext = image.filename.split('.')[-1]
        # Создаём случайное имя (на случай если пользователь использует небезопасное имя и на случай
        # если пользователи будут загружать файлы с одинаковыми именами)
        filename = token_urlsafe(16) + '.' + ext
        path = app.config['UPLOAD_FOLDER'] + '/' + filename
        # Если файл существует, создаём новое имя пока оно не будет уникальным
        while os.path.isfile(path):
            filename = token_urlsafe(16) + '.' + ext
            path = app.config['UPLOAD_FOLDER'] + '/' + filename
        image.save('static/' + path)

        return path


def secure_remove_image(image_path):
    if os.path.isfile('static/' + image_path):
        os.remove('static/' + image_path)
    else:
        flash('Файл не існує на сервері.', 'alert alert-danger')


def is_url_safe(target):
    if target is None:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
