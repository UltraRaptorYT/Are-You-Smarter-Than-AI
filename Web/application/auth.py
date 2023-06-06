from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user,current_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import json, jsonify
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 
    
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')    
    user = User.query.filter_by(email=email,username=username).first()
    if user: 
          flash('Email address already exists')
          return redirect(url_for('auth.signup'))

    new_user = User(email=email, username=username,
                    password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/api/signup", methods=['POST'])
def api_signup():
    data = request.get_json()
    email = data['email']
    if "@" not in email:
        flash('Invalid email address', "danger")
        
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(email=email,username=username).first()

    if user: 
        flash('Email address or username already exists', "danger")
        
    new_user = User(email=email, username=username,
                    password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id':new_user.id})

@auth.route("/api/login", methods=['POST'])
def api_login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'danger')
        return 0
    isLogin = login_user(user)
    return jsonify({"isLogin": isLogin})

@auth.route("/user/delete/<id>", methods=['POST'])
def api_del(id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "success"})
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0
    
