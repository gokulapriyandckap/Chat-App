from flask import Blueprint, render_template, request, flash,redirect,url_for
import re
from .models import User
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import sqlite3


# def get_db():
#     conn = sqlite3.connect('/home/dckapl108/Desktop/Files/python/Flask Projects/Login Signup/instance/database.db')
#     c = conn.cursor()
#     return c



auth = Blueprint('auth',__name__)

email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'


# def get_username(email):
#     c = get_db()
#     c.execute("select userName from user where email = '" + email + "'")
#     userName = (c.fetchall())
#     print(userName)
#     c.close()
@auth.route('/login', methods =['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # def get_username(email):
        #     c = get_db()
        #     c.execute("select userName from user where email =  email ")
        #     userName = (c.fetchone())
        #     print(userName[0])
        #     c.close()
        # get_username(email)
        user = User.query.filter_by(email=email).first()
        if user:

            if check_password_hash(user.password,password):
                flash(f"Logged in Successfully!",category='sucess')
                login_user(user,remember=True)

                # for fetch the username after login
                conn1 = sqlite3.connect('/home/dckapl108/Desktop/Files/python/Flask Projects/Login Signup/instance/database.db')
                c1 = conn1.cursor()
                c1.execute("select userName from user where email =  email ")
                userName = (c1.fetchone())
                print(userName[0])
                conn1.close()

                return redirect(url_for('views.homeView',userName=userName))
            else:
                flash('Incorrect Password :(, Try Again',category='error')
        else:
            flash('Email does not exist',category='error')

    return render_template('login.html', boolean = True,user=current_user)

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
            login_user(new_user, remember=True)
            print(new_user)
            flash("Account Created Successfully!",category='sucess')
            return redirect(url_for("views.homeView"))

    return render_template('sign_up.html',user=current_user)