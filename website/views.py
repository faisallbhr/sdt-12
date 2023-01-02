from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from . import db, app
from .models import Admin, User, Nota
import sqlite3
import os

views = Blueprint('views', __name__)

picFolder = os.path.join('static', 'pics')
app.config['UPLOAD_FOLDER'] = picFolder

@views.route('/', methods=['GET', 'POST'])
def user():
    pic1= os.path.join(app.config['UPLOAD_FOLDER'], '1.png')
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'], '2.png')
    pic3 = os.path.join(app.config['UPLOAD_FOLDER'], 'montir.png')

    conn = sqlite3.connect("./instance/db_antrian.db")
    curs = conn.cursor()
    
    curs.execute('SELECT * FROM user')
    cek = curs.fetchall()
    if cek == []:
        head = 1
        tail = 0
    else:
        cek_head = curs.execute('SELECT * FROM user ORDER by antrian asc')
        head = cek_head.fetchone()[1]

        cek_tail = curs.execute('SELECT * FROM user ORDER by antrian desc')
        tail = cek_tail.fetchone()[1]


    # CEK TAMPILAN NOTA
    cek_nota = curs.execute('SELECT * FROM nota WHERE antrian="{}"'.format(head-1))
    nota = cek_nota.fetchall()
    if nota == []:
        nota_nama = '-'
        nota_motor = '-'
        nota_plat = '-'
        nota_kerusakan = '-'
        nota_biaya = '-'
    else:
        for row in nota:
            nota_nama = row[1]
            nota_motor = row[2]
            nota_plat = row[3]
            nota_kerusakan = row[4]
            nota_biaya = row[5]

    
    # SAAT KLIK SERVIS
    if request.method == "POST":
        data = request.form.get("antrian")
        nama = request.form.get('nama')
        motor = request.form.get('motor')
        plat = request.form.get('plat')

        list_kerusakan = request.form.getlist('servicecbx')
        kerusakan = ''
        for rusak in list_kerusakan:
            kerusakan += rusak + ', '
        if len(nama) < 2 or len(motor) < 2 or len(plat) < 2 or len(kerusakan) < 2 :
            flash('Isikan semua data dengan benar', category='error')
            return redirect(url_for('views.user'))
        else:
            new_user = User(antrian=data,nama=nama.upper(), motor=motor.upper(), plat=plat.upper(), kerusakan=kerusakan.upper())
            db.session.add(new_user)
            db.session.commit()
            flash('Data telah ditambahkan', category='success')
            return redirect(url_for('views.user'))

    return render_template("home.html", img1=pic1, img2=pic2, img3=pic3, antrian=tail+1, panggil=head-1, user=current_user, nota_nama=nota_nama, nota_motor=nota_motor, nota_plat=nota_plat,nota_kerusakan=nota_kerusakan, nota_biaya=nota_biaya)


@views.route('/login', methods=['GET', 'POST'])
def login():
    pic1= os.path.join(app.config['UPLOAD_FOLDER'], '1.png')
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'], '2.png')
    pic3 = os.path.join(app.config['UPLOAD_FOLDER'], 'montir.png')


    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Admin.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('views.admin'))
        else:
            flash('Email atau password salah', category='error')
            return redirect(url_for('views.login'))

    return render_template('login.html', user=current_user, img1=pic1, img2=pic2, img3=pic3)


@views.route('/admin', methods=['GET', 'POST', 'DELETE'])
def admin():
    pic1= os.path.join(app.config['UPLOAD_FOLDER'], '1.png')
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'], '2.png')
    pic3 = os.path.join(app.config['UPLOAD_FOLDER'], 'montir.png')

    conn = sqlite3.connect("./instance/db_antrian.db")
    curs = conn.cursor()
    curs.execute('SELECT * FROM user')
    cek = curs.fetchall()
    if cek == []:
        head = 0
    else:
        curs.execute('SELECT * FROM user ORDER by antrian asc')
        head = curs.fetchone()[1]

    # CEK NOTA
    cek = curs.execute('SELECT * FROM user WHERE antrian="{}"'.format(head))
    cek = cek.fetchall()
    if cek == []:
        nama = '-'
        motor = '-'
        plat = '-'
        kerusakan = '-'
    else:
        for row in cek:
            nama = row[2]
            motor = row[3]
            plat = row[4]
            kerusakan = row[5]

    if request.method=='POST':
        # SAAT KLIK PANGGIL
        if request.form.get('next') == 'PANGGIL':
            data = request.form.get('panggil')
            total = request.form.get('total')
            
            cek_panggil = User.query.all()
            if cek_panggil == []:
                flash('Tidak ada antrian', category='error')
                return redirect(url_for('views.admin'))

            else:
                if total.isnumeric():
                    User.query.filter_by(antrian=data).delete()
                    new_nota = Nota(nama=nama.upper(), motor=motor.upper(), plat=plat.upper(), kerusakan=kerusakan.upper(), biaya=int(total), antrian=int(data))
                    db.session.add(new_nota)
                    cek = User.query.all()
                    if cek == []:
                        nota = Nota.query.all()
                        for i in range(len(nota)+1):
                            Nota.query.filter_by(id=(i+1)).delete()
                    db.session.commit()

                    return redirect(url_for('views.admin'))
                else:
                    flash('Masukkan total biaya dengan benar', category='error')
                    return redirect(url_for('views.admin'))

        # SAAT KLIK RESET NOTA
        if request.form.get('delete') == 'RESET':
            cek_user = User.query.all()
            for i in range(len(cek_user)+1):
                User.query.filter_by(id=(i+1)).delete()

            cek_nota = Nota.query.all()
            for i in range(len(cek_nota)+1):
                Nota.query.filter_by(id=(i+1)).delete()
                
            db.session.commit()
            flash('Data berhasil di reset', category='success')
            return redirect(url_for('views.admin'))

    return render_template('admin.html', img1=pic1, img2=pic2, img3=pic3, user=current_user, panggil=head, nama=nama, motor=motor, plat=plat, kerusakan=kerusakan)


@views.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.login'))