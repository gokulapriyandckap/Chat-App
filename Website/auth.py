# import dbus
from flask import Blueprint, render_template, request, flash,redirect,url_for
from .models import User
import re
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

@auth.route('/login', methods =['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Logged in Successfully!",category='sucess')
                login_user(user,remember=True)
                return redirect(url_for('views.homeView'))
            else:
                flash('Incorrect Password :(, Try Again',category='error')
        else:
            flash('Email Does not exist',category='error')

    return render_template('login.html', boolean = True)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        userName = request.form.get('userName')
        password = request.form.get('password')
        print(f"email:{email}",f"userName:{userName}",f"password:{password}")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email Already exist',category='error')
        elif len(email) < 5 and not re.match(email_pattern, email):
            flash("Hey Your Email is too short. Email Must be greater than 5", category='error' )
        elif len(userName) <2:
            flash("Hey Your Name is too short.", category='error' )
        elif  not not re.match(r'^[a-zA-Z]+$', userName):
            flash("User Name should Contains one  Upper and Lower Case Letter", category='error')
        elif  not re.search(r'[_-]', userName):
            flash("User Name should Contains underscore or Hyphen  ", category='error')
        elif len(password) < 8:
            flash("Password Must be at Least 7 Character", category='error' )
        elif not re.search(r'[A-Z]',password):
            flash("Password Must be Contains one Upper Case Letter", category='error')
        elif not  re.search(r'[a-z]', password):
            flash("Password Must be Contains one Lower Case Letter", category='error')
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            flash("Password Must be Contains one special Character", category='error')
        elif not re.search(r'\d', password):
            flash("Password Must be Contains atleast one number", category='error')
        else:
            new_user = User(email=email, userName=userName, password=generate_password_hash(password,method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            # login_user(user, remember=True)
            print(new_user)
            flash("Account Created Successfully!",category='sucess')
            return redirect(url_for("views.homeView"))

    return render_template('sign_up.html')