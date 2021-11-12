from app import *


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    last_login = db.Column(db.DateTime, unique=False, nullable=True)

    def __repr__(self):
        return f"{self.id=}, {self.username=}, {self.password=}, {self.last_login=}"


db.create_all()
