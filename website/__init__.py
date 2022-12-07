from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager, UserMixin


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_antrian.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    # from .models import Admin
    # login_manager = LoginManager
    # login_manager.login_view = 'views.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return Admin.query.get(int(id))

    return app