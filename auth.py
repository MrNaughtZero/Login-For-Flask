from flask import Flask, Blueprint, render_template, abort, flash, get_flashed_messages, redirect, url_for, request
from app.forms import UserRegister, UserLogin
from app.models import User
from app import app
from flask_login import login_user, logout_user

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route('/login', methods=['GET'])
def login():
    return render_template('/auth/login.html', form=UserRegister(), title="Login", error=get_flashed_messages())

@auth_bp.route('/login/attempt', methods=['POST'])
def login_attempt():
    usr = User(username=request.form.get('username'), password=User.hash_password(request.form.get('password'))).queryUser()
    if not usr:
        flash('Incorrect Login Details')
        return redirect(url_for('auth_bp.login'))
    else:
        login_user(usr)
        return redirect(url_for('main_bp.dashboard'))


@auth_bp.route('/register', methods=['GET'])
def register():
    return render_template('/auth/register.html', form=UserRegister(), title="Register", error=get_flashed_messages())

@auth_bp.route('/register/new/user', methods=['POST'])
def register_user():
    if request.form.get('password') != request.form.get('confirm_password'):
        flash('Passwords do not match')
        return redirect(url_for('auth_bp.register'))

    if not UserRegister().validate_on_submit():
        flash('Something went wrong')
        return redirect(url_for('auth_bp.register'))

    if request.form.get('secret_key') != app.config['SECRET_KEY']:
        flash('Something went wrong.')
        return redirect(url_for('auth_bp.register'))

    User(username=request.form.get('username'), password=User.hash_password(request.form.get('password'))).create_user()
    
    flash('Account Created. Please login to continue')
    return redirect(url_for('auth_bp.login'))