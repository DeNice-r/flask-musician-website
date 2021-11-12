from app import *


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    last_updated = db.Column(db.DateTime, unique=False, nullable=True)

    def __repr__(self):
        return f"{self.id=}, {self.image=}, {self.name=}, {self.year=}, {self.last_updated=}"
