import datetime
import os

from flask import render_template, request, redirect, flash, url_for
from app import app, db
from models.album import Album
from flask_login import login_required
from utils import secure_save_image, secure_remove_image
from flask_login import current_user


@app.route('/albums')
def albums():
    return render_template("albums.html", app=app, user=current_user,
                           albums=Album.query.order_by(Album.year.desc()).all())


@app.route('/album_update', methods=['GET', 'POST'])
@login_required
def album_update():
    query_album_id = request.args.get('album_id')
    # Если айди есть то
    if query_album_id:
        # То получаем список альбомов с этим айди
        current_album = Album.query.get(query_album_id)
        # Если такового нету то
        if current_album is None:
            # Выводим об этом сообщение
            flash('Альбом з таким ідентифікатором не знайдено.', 'alert alert-danger')
        # Если таковой есть
        else:  # isinstance(current_album, Album)
            # и метод пост
            if request.method == 'POST':
                form_name = request.form['name']
                form_year = request.form['year']
                # а так же все данные переданы (на случай пост-запроса не через форму)
                if not (form_name and form_year.isdigit()):
                    flash('Невірне значення імені або року.', 'alert alert-danger')
                    return redirect('/album_update')
                # то нам нужно отредактировать его в бд
                if 'image' in request.files:
                    image = request.files['image']
                    # если картинка подходит
                    saved_path = secure_save_image(image)
                    if saved_path is not None:
                        secure_remove_image(current_album.image)
                        current_album.image = saved_path
                current_album.name = request.form['name']
                current_album.year = request.form['year']
                current_album.last_updated = datetime.datetime.now()
                db.session.commit()
                flash('Альбом успішно оновлено.', 'alert alert-success')
            # и метод гет
            else:  # request.method == 'GET'
                # и есть аргумент удалить
                if request.args.get('delete') == '1':
                    # то удалить
                    # сначала картинку
                    secure_remove_image(current_album.image)
                    # потом данные из бд
                    db.session.delete(current_album)
                    db.session.commit()
                    flash('Альбом успішно видалено.', 'alert alert-success')
                # иначе
                else:  # request.args.get('delete') is None
                    # нужно передать его данные в темплейт
                    return render_template('album_update.html', app=app, user=current_user, current_album=current_album)

        # Если дошли сюда, то перенаправляем на страницу с альбомами
        return redirect('/albums')
        # return render_template('album_update.html', app=app, current_album=current_album)

    # Если метод пост
    if request.method == 'POST':
        form_name = request.form['name']
        form_year = request.form['year']
        # и в переданных файлах нету image
        if 'image' not in request.files:
            # Выводим соответствующую ошибку
            flash('Файл не знайдено.', 'alert alert-danger')
            return render_template('album_update.html', app=app, user=current_user)
        if not (form_name and form_year.isdigit()):
            flash('Невірне значення імені або року.', 'alert alert-danger')
            return render_template('album_update.html', app=app, user=current_user)

        # и в переданных файлах есть image, получаем картинку
        image = request.files['image']
        # пытаемся сохранить
        saved_path = secure_save_image(image)
        # если сохранить получилось
        if saved_path is not None:
            # то сохраняем новый альбом в бд
            alb = Album(image=saved_path, name=form_name, year=form_year, last_updated=datetime.datetime.now())
            db.session.add(alb)
            db.session.commit()
            flash('Альбом успішно додано.', 'alert alert-success')
        return redirect('/album_update')

    return render_template('album_update.html', app=app, user=current_user)
