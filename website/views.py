from flask import Blueprint, render_template, request
from . import db, User, MyQueue
import sqlite3

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def user():
    q = MyQueue()
    antrian = q.enqueue()
    pengambilan = q.dequeue()
    
    if request.method == "POST":
        data = request.form.get("antrian")
        new_user = User(antrian=data)
        db.session.add(new_user)
        db.session.commit()
    return render_template("home.html",antrian=antrian, pengambilan=pengambilan)


@views.route('/admin', methods=['GET', 'POST'])
def admin():
    # conn = sqlite3.connect("./instance/db_antrian.db")
    # curs = conn.cursor()
    # curs.execute('SELECT * FROM user ORDER by antrian asc LIMIT 1')
    # dequeue = curs.fetchone()[1]
    q = MyQueue()
    antrian = q.enqueue()
    panggil = q.dequeue()
    if request.method=='POST':
        data = request.form.get('panggil')
        User.query.filter_by(antrian=data).delete()
        db.session.commit()
        
    return render_template('admin.html', panggil=panggil, antrian=antrian)