import datetime

from flask import Flask, render_template, redirect
from app import app, db
from models.album import Album


class AlbumContainer:
    def __init__(self, image, name, year_of_release):
        self.image = image
        self.name = name
        self.year_of_release = year_of_release


@app.route('/albums')
def albums():
    print(Album.query.all())
    return render_template("albums.html", app=app, albums=Album.query.all())


# Add object to db
# alb = Album(image='киш.jpg', name='Ну тупо альбом', year=2007, last_updated=datetime.datetime.now())
# db.session.add(alb)
# db.session.commit()
