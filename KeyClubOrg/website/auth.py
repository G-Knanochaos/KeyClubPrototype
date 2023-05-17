from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route('login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                n = request.args.get("next")
                if n: 
                    return redirect(n)
                else:
                    return redirect(url_for("views.home"))
            else:
                flash('Incorrect password. Try again hacker.', category = 'error')
        else:
            flash('Email does not exist', category = 'error')
    else:
        return render_template("login.html", user=current_user)


@auth.route('sign-up', methods = ['GET','POST'])
def signup():
    if current_user.is_authenticated: 
        return redirect(url_for("views.default"))
    else: 
        if request.method == 'POST':
            print("Retreiving User Info!")
            email = request.form.get('email-input')
            username = request.form.get('name-input')
            password1 = request.form.get('password-input')
            password2 = request.form.get('confirm-password')
            print("User Info Retreived!")


            user = User.query.filter_by(email=email).first()
            name = User.query.filter_by(username=username).first()
            if user:
                flash('Email already exists. Please try again.', category = 'error')
            elif name:
                flash('Username already exists. Please try again.', category= 'error')
            elif len(email) < 4:
                flash('Email must be longer than 3 characters. Please try again.', category = 'error')
            elif len(username) < 2:
                flash('User name must be longer than 1 character. Please try again.', category = 'error')
            elif password1 != password2:
                flash("Passwords don't match. Please try again.", category = 'error')
            elif len(password1) < 7:
                flash('Password must be at least 7 characters. Please try again.', category = 'error')
            else:
                new_user = User(email=email,
                    username=username, 
                    password=generate_password_hash(password1, method='sha256'), 
                    school = request.form.get('school-input')
                    )
                db.session.add(new_user)
                db.session.commit()
                flash('Account Created!', category = 'success')
                login_user(new_user, remember=True)
                return redirect(url_for('views.default'))
        return render_template("sign-up.html", user=current_user)


@auth.route('logout')
@login_required #makes it so that the user cannot visit the page without being logged 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))