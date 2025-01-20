from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import db
from app.models.user import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

user_routes = Blueprint('users', __name__)

@user_routes.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        login_email = request.form.get('user_email')
        password = request.form.get('password')
        name = request.form.get('name')
        last_name = request.form.get('surname')

        if not login_email or not password or not name or not last_name:
            return render_template('create_user.html', error="All required fields must be filled in!")
    
        if User.query.filter(User.login_email == login_email).first():
             return render_template('create_user.html', error="The email you entered is already registered, please try another one.")
    
        password_hash = generate_password_hash(password)
        new_user = User(name=name, last_name = last_name, login_email= login_email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.")
        return redirect(url_for('users.login'))
    

    return render_template('create_user.html')

@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(login_email=login_email).first()
        if user and check_password_hash(user.password, password):
            if not user.is_active or user.is_deleted:
                return render_template('login.html', error="Your account is curently blocked or deleted.")
            
            login_user(user)  # user login using flask-login built in function
            flash("Login successful.")
            return redirect(url_for('users.dashboard'))
        else:
            return render_template('login.html', error="Invalid email or password entered.")

    return render_template('login.html')

@user_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out!")
    return redirect(url_for('users.login'))

@user_routes.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('users.admin_dashboard'))
    else:
        return redirect(url_for('users.user_dashboard'))
    
@user_routes.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('users.dashboard'))
    return "Admin Dashboard!" #This can be changed to something more likeable


@user_routes.route('/user_dashboard')
@login_required
def user_dashboard():
    if current_user.is_admin:
        return redirect(url_for('users.admin_dashboard'))
    return "User Dashboard!" #This can be changed to something more likeable