from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, current_user
from . import db
from .models import Admin, User, MyQueue

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
        return redirect(url_for('views.user'))
    return render_template("home.html",antrian=antrian, pengambilan=pengambilan)


@views.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if request.method=='POST':
        user = Admin.query.filter_by(email=email, password=password).first()
        if user:
            # login_user(user, remember=True)
            return redirect(url_for('views.admin'))
    return render_template('login.html', user=current_user)


@views.route('/admin', methods=['GET', 'POST'])
# @login_required
def admin():
    q = MyQueue()
    antrian = q.enqueue()
    panggil = q.dequeue()
    if request.method=='POST':
        data = request.form.get('panggil')
        User.query.filter_by(antrian=data).delete()
        db.session.commit()
        return redirect(url_for('views.admin'))
    return render_template('admin.html', user=current_user, panggil=panggil, antrian=antrian)  