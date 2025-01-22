from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, jsonify
from sqlalchemy import or_, and_
from app.database import db
from app.models.user import User
from app.models.order import Order
from app.models.transaction import Transaction
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=braintree.Environment.Sandbox,
        merchant_id="t7mvc2hrv49kmwg2",
        public_key="mgp382dhthfvqr6q",
        private_key="eb3626bf4b2a07916a35a3fdd94ee293"
    )
)

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

@bp.route('/get_client_token', methods=['GET'])
@login_required
def get_client_token():
    client_token = gateway.client_token.generate()
    return jsonify({"client_token": client_token})

@bp.route('/users')
def home():
    return render_template('user/user_index.html')

@bp.route('/register', methods = ['GET','POST'])
def register():

    form=RegistrationForm()
    
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        login_email = form.email.data
        password = form.password.data
        
        password_hash = generate_password_hash(password) 
        new_user = User(name, surname, login_email, password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash(f"Welcome {name}! Your registration is successful, you can now log in")
        return redirect(url_for('users.login'))
      
    return render_template('user/user_register_extends_base.html', form=form)

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
                return render_template('user/user_login_extends_base.html', form=form)
            
            login_user(user)  # user login using flask-login built in function

            return redirect(url_for('users.dashboard'))
        else:
            flash("Invalid email or password")
            return render_template('user/user_login_extends_base.html', form = form)
        
    return render_template('user/user_login_extends_base.html', form = form)


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
    return render_template('admin/admin_layout.html') 


@bp.route('/user_dashboard')
@login_required
def user_dashboard():
    if current_user.is_admin:
        return redirect(url_for('users.admin_dashboard'))
    client_token = gateway.client_token.generate()
    return render_template('user/user_layout.html', client_token=client_token) 


@bp.route('/transactions')
@login_required
def show_transactions():
    if current_user.is_admin:
        # Admins see all transactions
        transactions = Transaction.query.all()
        return render_template('admin/view_all_transactions.html', transactions=transactions)  # Admin template
    else:
        # Regular user sees only their own transactions
        transactions = Transaction.query.filter_by(user_id=current_user.id).all()
        return render_template('user/user_transactions.html', transactions=transactions)

@bp.route('/admin/all_users')
@login_required
def show_users():
    if not current_user.is_admin:
        abort(403)   
    users = User.query.all()
    return render_template('admin/view_users.html', users=users)

@bp.route('/orders')
@login_required
def show_orders():
    if current_user.is_admin:
        # Admin sees all orders
        orders = Order.query.all()
        return render_template('admin/view_orders.html', orders=orders)  # Admin template
    else:
        # Regular user sees only their own orders
        orders = Order.query.filter_by(user_id=current_user.id).all()
        return render_template('user/view_orders.html', orders=orders)
    
@bp.route('/add_balance', methods=['POST'])
@login_required
def add_balance():
    try:
        amount = request.form.get('amount')
        nonce = request.form.get('payment_method_nonce')

        if not amount or not nonce:
            flash("Invalid input. Please try again.", "danger")
            return redirect(url_for('users.user_dashboard'))

        amount = float(amount)

        if amount <= 0:
            flash("Amount must be greater than 0.", "danger")
            return redirect(url_for('users.user_dashboard'))
        
        result = gateway.transaction.sale({
            "amount": f"{amount:.2f}",
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })

        if result.is_success:
            # Update user's balance
            current_user.balance += amount

            transaction = Transaction(user_id=current_user.id, sum=amount, status="Completed")
            db.session.add(transaction)
            db.session.commit()

            flash(f"Successfully added {amount}€ to your balance!", "success")
        else:
            transaction = Transaction(user_id=current_user.id, sum=amount, status="Failed")
            db.session.add(transaction)
            db.session.commit()

            flash(f"Payment failed: {result.message}", "danger")

    except ValueError:
        flash("Invalid amount entered. Please enter a valid number.", "danger")
    except Exception as e:
        print(f"Error during add_balance: {e}")
        flash("An error occurred. Please try again later.", "danger")

    return redirect(url_for('users.user_dashboard'))


@bp.route('/cash_out', methods=['POST'])
@login_required
def cash_out():
    try:
        amount = request.form.get('amount')

        if not amount:
            flash("Invalid input. Please try again.", "danger")
            return redirect(url_for('users.user_dashboard'))

        amount = float(amount)

        if amount <= 0:
            flash("Amount must be greater than 0.", "danger")
            return redirect(url_for('users.user_dashboard'))

        # Check if user has sufficient balance
        if current_user.balance < amount:
            flash("Insufficient balance to complete the cash out.", "danger")
            return redirect(url_for('users.user_dashboard'))

        # Deduct amount from user's balance
        current_user.balance -= amount

        transaction = Transaction(user_id=current_user.id, sum=-amount, status="Completed")
        db.session.add(transaction)
        db.session.commit()

        flash(f"Successfully cashed out {amount}€ from your balance!", "success")
    except ValueError:
        flash("Invalid amount entered. Please enter a valid number.", "danger")
    except Exception as e:
        print(f"Error during cash_out: {e}")
        flash("An error occurred. Please try again later.", "danger")

    return redirect(url_for('users.user_dashboard'))
