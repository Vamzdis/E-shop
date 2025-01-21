from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.database import db
from app.models.user import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

bp = Blueprint('users', __name__)

@bp.route('/register', methods = ['GET','POST'])
def register():

    form=RegistrationForm()
    
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        login_email = form.email.data
        password = form.password.data
    
        if User.query.filter(User.login_email == login_email).first():
            return render_template('user_register_extends_base.html', form=form, error="The email you entered is already registered, please try another one.")
        
        password_hash = generate_password_hash(password) 
        new_user = User(name, surname, login_email, password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.")
        return redirect(url_for('users.login'))

    return render_template('user_register_extends_base.html', form=form)
 

@bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        login_email = form.email.data
        password = form.password.data

        user = User.query.filter_by(login_email=login_email).first()
        if user and check_password_hash(user.password, password):
            if not user.is_active or user.is_deleted:
                return render_template('user_login_extends_base.html', form = form , error="Your account is curently blocked or deleted.")
            
            login_user(user)  # user login using flask-login built in function
            flash("Login successful.")
            return redirect(url_for('users.dashboard'))
        else:
            return render_template('user_login_extends_base.html', form = form ,error="Invalid email or password entered.")
        
    return render_template('user_login_extends_base.html', form = form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out!")
    return redirect(url_for('users.login'))


@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('users.admin_dashboard'))
    else:
        return redirect(url_for('users.user_dashboard'))
    

@bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('users.dashboard'))
    return render_template('admin_dashboard.html') #This can be changed to something more likeable



@bp.route('/user_dashboard')
@login_required
def user_dashboard():
    if current_user.is_admin:
        return redirect(url_for('users.admin_dashboard'))
    return render_template('user_dashboard.html') #This can be changed to something more likeable