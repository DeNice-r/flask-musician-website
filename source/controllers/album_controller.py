import datetime
from flask import render_template, request, redirect, flash
from app import app, db
from models.album import Album
from flask_login import login_required
from utils import secure_save_image, secure_remove_image
from flask_login import current_user


@app.route('/albums')
def albums():
    return render_template("albums.html",
                           # Передаємо альбоми відсортовані за роком виходу від найновіших
                           albums=Album.query.order_by(Album.year.desc()).all())


@app.route('/album_update', methods=['GET', 'POST'])
@login_required
def album_update():
    query_album_id = request.args.get('album_id')
    # Якщо є айді то
    if query_album_id:
        # Отримуємо альбом з цим айді
        current_album = Album.query.get(query_album_id)
        # Якщо такого альбому немає
        if current_album is None:
            # виводимо про це повідомлення
            flash('Альбом з таким ідентифікатором не знайдено.', 'alert alert-danger')
        # Якщо такий є
        else:  # isinstance(current_album, Album)
            # і метод пост
            if request.method == 'POST':
                form_name = request.form['name']
                form_year = request.form['year']
                # а також всі дані передано (на випадок пост-запиту не через форму)
                if not (form_name and form_year.isdigit()):
                    flash('Невірне значення імені або року.', 'alert alert-danger')
                    return redirect('/album_update')
                # та картинка є у запиті
                if 'image' in request.files:
                    image = request.files['image']
                    # і її вдалося зберегти
                    saved_path = secure_save_image(image)
                    if saved_path is not None:
                        # то стару (якщо вона є) та записуємо нову
                        secure_remove_image(current_album.image)
                        current_album.image = saved_path
                # Зберігаємо ім'я, рік та нову дату оновлення
                current_album.name = request.form['name']
                current_album.year = request.form['year']
                current_album.last_updated = datetime.datetime.now()
                # Та оновлюємо дані у бд
                db.session.commit()
                flash('Альбом успішно оновлено.', 'alert alert-success')
            # та метод гет
            else:  # request.method == 'GET'
                # і є аргумент "видалити"
                if request.args.get('delete') == '1':
                    # то видалити
                    # спочатку картинку
                    secure_remove_image(current_album.image)
                    # потім дані з бд
                    db.session.delete(current_album)
                    db.session.commit()
                    flash('Альбом успішно видалено.', 'alert alert-success')
                # коли аргумента видалити немає
                else:  # request.args.get('delete') is None
                    # потрібно передати його дані у темплейт
                    return render_template('album_update.html', current_album=current_album)

        # Якщо дойшли сюди, то перенаправляємо на сторінку з альбомами
        return redirect('/albums')

    # Якщо метод пост
    if request.method == 'POST':
        form_name = request.form['name']
        form_year = request.form['year']
        # і в переданих файлах немає картинки
        if 'image' not in request.files:
            # Виводимо помилку
            flash('Файл не знайдено.', 'alert alert-danger')
            return render_template('album_update.html')
        # Якщо назва альбому та рік підходять
        if not (form_name and form_year.isdigit()):
            # виводимо про це помилку
            flash('Невірне значення імені або року.', 'alert alert-danger')
            return render_template('album_update.html')

        # та в переданих файлах є картинка, отримуємо її
        image = request.files['image']
        # намагаємося зберегти
        saved_path = secure_save_image(image)
        # якщо це вдалося
        if saved_path is not None:
            # то зберігаємо новий альбом у бд
            alb = Album(image=saved_path, name=form_name, year=form_year, last_updated=datetime.datetime.now())
            db.session.add(alb)
            db.session.commit()
            # і виводимо про це повідомлення
            flash('Альбом успішно додано.', 'alert alert-success')
        return redirect('/album_update')
    # Якщо жодна з умов не виконалася, просто завантажуємо сторінку
    return render_template('album_update.html')
