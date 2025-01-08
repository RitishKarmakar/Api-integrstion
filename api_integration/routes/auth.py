from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check for existing user
        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for('auth.signup'))

        # Check password match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('auth.signup'))

        # Create new user
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please sign in.", "success")
        return redirect(url_for('auth.signin'))

    return render_template('signup.html')


@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['email'] = user.email
            flash("Signed in successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password!", "danger")
            return redirect(url_for('auth.signin'))

    return render_template('signin.html')


@auth_bp.route('/signout')
def signout():
    session.clear()
    flash("Signed out successfully!", "success")
    return redirect(url_for('index'))
