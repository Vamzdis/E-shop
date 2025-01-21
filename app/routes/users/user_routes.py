from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from sqlalchemy import or_, and_
from app.database import db
from app.models.user import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError

#custom validator at registration to check if the email has already been registered
class EmailRegistered(object):
    
    def __init__(self, message=None):

        if not message:
            message = "The email you've entered is already registered."
        self.message = message

    def __call__(self, form, field):
        email = field.data
        if User.query.filter(User.login_email == email).first():
            if User.query.filter(
                User.login_email == email,
                or_(
                    User.is_active == False,  
                    User.is_deleted == True)).first():
                #if the user with this email was blocked or deleted already it would show this message
                raise ValidationError(message="This email is already associated with a blocked or deleted account.")
            
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email(), EmailRegistered()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_\-+=\[\]{}|\\:;"\'<>,.?/~`])',
                                                    message="""The password must contain at least one 
                                                    lower case letter, 
                                                    upper case letter,
                                                    number and a 
                                                    special character
                                                    """)])
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

        # if User.query.filter(User.login_email == login_email).first():
        #     flash("The email you've entered ir registered already")
        #     return render_template('user_register_extends_base.html', form=form)
        
        password_hash = generate_password_hash(password) 
        new_user = User(name, surname, login_email, password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash(f"Welcome {name}! Your registration is successful, you can now log in")
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
            if user.is_deleted or not user.is_active:
                form.email.errors.append("This account is blocked or deleted.")
                return render_template('login.html', form=form)
            
            # if not user.is_active or user.is_deleted:
            #     flash("Your account is blocked or deleted")
            #     return render_template('user_login_extends_base.html', form = form)
            
            login_user(user)  # user login using flask-login built in function

            flash("Login successful.")
            return redirect(url_for('users.dashboard'))
        else:
            flash("Invalid email or password")
            return render_template('user_login_extends_base.html', form = form)
        
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