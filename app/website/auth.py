from flask import Blueprint, render_template, request, flash, jsonify, Flask, redirect, url_for
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from .models import user
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .res.mymail import *
import re
from .forms import LoginForm
import random, string
# Make a regular expression
# for validating an Email
regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        print(email, flush=True)
        testuser = user.query.filter_by(email=email).first()
        if testuser:
            if check_password_hash(testuser.password, password):
                if not testuser.is_activated:
                    flash('Account is not activated, please check email', category='error')
                else:
                    login_user(testuser, remember=False)
                    return redirect(url_for('dashboard.dash'))
            else:
                 flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exsist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return "Logged out"

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        fname = request.form.get('fname')
        sname = request.form.get('sname')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')

        test_user = user.query.filter_by(email=email).first()
        if test_user:
            flash("Email Already Exsists, Please enter a different email address", category='error')
        elif(not re.fullmatch(regex_email, email)):
            flash("Invalid Email Address", category='error')
        elif password != cpassword:
            flash("Passwords do not match", category='error')
        elif len(password) < 8:
            flash("Password must be longer than 8 charecters", category='error')
        else:
            print("user valid", flush=True)
            #print(generateAuthToken(), flush=True);
            auth_token=generateAuthToken()
            new_user = user(email=email, first_name=fname, second_name=sname, password=generate_password_hash(
                password, method='sha256'), activation_token=auth_token, is_activated=False )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration Successful, Please check email to activate account", '')
            mail = mymail()
            mail.setToEmail(email)
            mail.setSubject("Activate Account")
            mail.setMessage("Visit: localhost:5000/account/activate?token=" + auth_token)
            mail.send()
    return render_template("register.html", user=current_user)

def generateAuthToken():
    validToken = False
    token=''
    while not validToken:
        letters=string.ascii_lowercase
        token= ''.join(random.choice(letters) for i in range(12))
        testuser = user.query.filter_by(activation_token=token).first()
        if not testuser:
            validToken=True
    return token

@auth.route('/account/activate', methods=['GET'])
def activateAccount():
    token = request.args.get('token')
    testuser = user.query.filter_by(activation_token=token).first()
    isValid=False
    if testuser:
        testuser.is_activated = True
        isValid = True
        db.session.commit()
    return render_template("activate_account.html", user=current_user, accountActivate=isValid)





#from main import app