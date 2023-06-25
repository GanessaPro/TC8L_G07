from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    print("Please login using your registered username and password")
    return render_template('login_page.html')

@auth.route('/login', methods=['POST'])
def login_post():
    #print('Inside login post')
    # login code goes hereemail = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username = username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        print("'Please check your login details and try again.'")
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    session.clear()
    session['username'] = user.username
    session['user_id'] = user.id
    print('Login successfull username is',user.username, 'and your id is', user.id)

    #check if the user is customer or admin
    if user.role == 'Admin':
        print("Welcome admin")
        return redirect(url_for('admin.dashboard'))
    else:
        print(f"Hello {session['username']}! ,This is the buy menu page ")
        return redirect(url_for('customer.main_page_customer'))

@auth.route('/signup')
def signup():
    print("Please fill up the registartion form, make sure remember your username and password")
    return render_template('registration_page.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    gender = request.form.get('gender')
    if gender == 'male':
        gender = 'male'
    elif gender == "female":
        gender = 'female'
    else:
        gender = 'none'
    fullname = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    phone_num = request.form.get('phonenumber')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    
    # print(f"Fullname: {fullname} \nUsername: {username}\nE-mail: {email}\nPhone Number: {phone_num}\nPassword: {password}\nConfirm Password: {confirm_password}\nGender: {gender}")
    
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        print("The email is already taken by other customer, please try a different email")
        return redirect(url_for('auth.signup'))
    
    if User.query.filter_by(username=username).first(): # if a user is found, we want to redirect back to signup page so user can try again
        flash('Username already taken')
        print("The username is already taken by other customer, please try a different username")
        return redirect(url_for('auth.signup'))


    password =  generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User( fullname=fullname, username=username,  password=password, email=email, phonenum = phone_num, gender=gender, role='Customer')
    
    # add the new user to the database
    # the new_user will be added in users table
    db.session.add(new_user)
    db.session.commit()
    print("Successfully registered as a customer")
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    logout_user()
    session.clear()
    print("Successfully logged out ")
    return redirect(url_for('main.index'))