from app import db


# Створюємо модель альбома
class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.DateTime, unique=False, nullable=True)
