from flask import Blueprint, render_template, request, session, redirect, url_for
from app.database import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('users', __name__)

@bp.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        user_email = request.form.get('user_email')
        password = request.form.get('password')
        name = request.form.get('name')
        surname = request.form.get('surname')
        is_admin = request.form.get('is_admin', 'false').lower() == 'true'

        if not user_email or not password or not name or not surname:
            return render_template('create_user.html', error="All required fields must be filled in!")
    
        if User.query.filter((User.login_email == user_email) | (User.password == password)).first():
             return render_template('create_user.html', error="The email you entered is already registered, please try another one.")
    
        password_hash = generate_password_hash(password_hash)
        new_user = User(user_email=user_email, password=password_hash, name=name, surname=surname, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('create_user.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid email or password entered.")

    return render_template('login.html') 

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))