from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager, UserMixin
from os import path


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_antrian.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0
    app.secret_key = b'SDT-12'
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .models import Admin
    login_manager = LoginManager()
    # login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    return app

# if not path.exists('instance/db_antrian.db'):
#     class User(db.Model):
#         __tablename__ = 'user'
#         id = db.Column(db.Integer, primary_key=True)
#         antrian = db.Column(db.Integer)
#         kerusakan = db.relationship('Kerusakan')

#     class Kerusakan(db.Model):
#         __tablename__ = 'kerusakan'
#         id = db.Column(db.Integer, primary_key=True)
#         kerusakan = db.Column(db.String(100))
#         user_antrian = db.Column(db.Integer, db.ForeignKey('user.antrian'))

#     class Admin(db.Model, UserMixin):
#         __tablename__ = 'admin'
#         id = db.Column(db.Integer, primary_key=True)
#         email = db.Column(db.String(50))
#         password = db.Column(db.String(50))