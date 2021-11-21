from app import app
from flask import request, flash
from secrets import token_urlsafe
from urllib.parse import urlparse, urljoin
import os


def is_picture(filename: str):
    # Перевіряємо, чи картинка прийнятна по її розширенню
    if '.' in filename:
        split = filename.rsplit('.', 1)
        if len(split) == 2:
            return split[1].lower() in app.config['PICTURE_EXTENSIONS']
    return False


def secure_save_image(image):
    # якщо картинка підходить
    if is_picture(image.filename):
        # завантажуємо її
        # Для початку, отримуємо розширення
        ext = image.filename.split('.')[-1]
        # Створюємо випадкове ім'я файлу (на випадок не безпечного імені файлу або кількох файлів з одним ім'ям)
        filename = token_urlsafe(16) + '.' + ext
        path = app.config['UPLOAD_FOLDER'] + '/' + filename
        # Якщо ім'я зайняте, створюємо нове поки воно не буде унікальним
        while os.path.isfile(path):
            filename = token_urlsafe(16) + '.' + ext
            path = app.config['UPLOAD_FOLDER'] + '/' + filename
        # коли знайшли підходяще ім'я, зберігаємо картинку з цим іменем та повертаємо ім'я файла
        image.save('static/' + path)
        return path


def secure_remove_image(image_path):
    # Якщо файл існує
    if os.path.isfile('static/' + image_path):
        # То видаляємо його
        os.remove('static/' + image_path)
    else:
        # У іншому випадку виводимо повідомлення про те, що нічого видаляти
        flash('Файл не існує на сервері.', 'alert alert-danger')


def is_url_safe(target):
    # Перевіряємо, чи URL передане
    if target is None:
        return False
    # Перевіряємо, чи прямує URL на наш сайт, якщо це не так, то воно не безпечне
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
