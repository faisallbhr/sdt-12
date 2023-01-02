from . import db
from flask_login import UserMixin

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    antrian = db.Column(db.Integer)
    nama = db.Column(db.String(50))
    motor = db.Column(db.String(50))
    plat = db.Column(db.String(50))
    kerusakan = db.Column(db.String(100))

class Nota(db.Model):
    __tablename__ = 'nota'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    motor = db.Column(db.String(50))
    plat = db.Column(db.String(50))
    kerusakan = db.Column(db.String(100))
    biaya = db.Column(db.Integer)
    antrian = db.Column(db.Integer)

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
