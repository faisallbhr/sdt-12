from . import db
import sqlite3
from flask_login import UserMixin

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    antrian = db.Column(db.Integer)
    kerusakan = db.relationship('Kerusakan')

class Kerusakan(db.Model):
    __tablename__ = 'kerusakan'
    id = db.Column(db.Integer, primary_key=True)
    kerusakan = db.Column(db.String(100))
    user_antrian = db.Column(db.Integer, db.ForeignKey('user.antrian', ondelete='SET NULL'))

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

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
        temp = self.head

        self.head = self.head.next
        if (self.head == None):
            self.tail = None
        return temp.data

    def tail_node(self):
        if (self.head == None):
            print("Empty Queue")
            return -1

        return self.tail.data