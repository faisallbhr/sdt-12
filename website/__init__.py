from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import sqlite3

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

    return app

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    antrian = db.Column(db.Integer)

class QNode:
    def __init__(self, value):
        self.data = value
        self.next = None

class MyQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self):
        conn = sqlite3.connect("./instance/db_antrian.db")
        curs = conn.cursor()
        # user = User.query.all()
        curs.execute('SELECT * FROM user ORDER by antrian asc')
        head = curs.fetchone()[1]
        head_node = QNode(int(head))

        curs.execute('SELECT * FROM user ORDER by antrian desc')
        tail = curs.fetchone()[1]
        tail_node = QNode(int(tail)+1)

        self.head = head_node
        self.head.next = tail_node
        self.tail = tail_node

        return self.tail.data

    def dequeue(self):
        # if (self.head == None):
        #     print("Empty Queue")
        #     return 'tes'

        temp = self.head

        if temp.data == None:
            return 'Antrian Habis'

        self.head = self.head.next
        if (self.head == None):
            self.tail = None
        return temp.data
