from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from sqlalchemy import or_
from app.database import db
from app.models.user import User
from app.models.order import Order
from app.models.product import Product
from app.models.transaction import Transaction
from app.models.product_cart import ProductCart
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
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

bp = Blueprint('users', __name__)

@bp.route('/get_client_token', methods=['GET'])
@login_required
def get_client_token():
    client_token = gateway.client_token.generate()
    return jsonify({"client_token": client_token})

@bp.route('/register', methods = ['GET','POST'])
def register():

    form=RegistrationForm()
    
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        login_email = form.email.data
        password = form.password.data
        
        password_hash = generate_password_hash(password) 
        new_user = User(name=name, last_name=surname, login_email=login_email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash(f"Welcome {name}! Your registration is successful, you can now log in", "success")
        return redirect(url_for('users.login'))
      
    return render_template('user/user_register_extends_base.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        login_email = form.email.data
        password = form.password.data

        user = User.query.filter_by(login_email=login_email).first()
        
        if user:
            if user.is_deleted or not user.is_active:
                form.email.errors.append("This account is blocked or deleted.")
                return render_template('user/user_login_extends_base.html', form=form)
            if user.failed_login_count >= 3:
                form.email.errors.append("This account is locked due too many incorrect login attempts. Please contact the administrator")
            if check_password_hash(user.password, password):
                user.failed_login_count = 0
                login_user(user)  
                flash("You have successfully logged in!", "success")
                db.session.commit()

                #handling rerouting here
                next_page = request.args.get('next')

                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('shop.show'))
                
            else:
                user.failed_login_count += 1
                if user.failed_login_count >= 3:
                    user.is_active = False
                    form.email.errors.append("This account is locked due too many incorrect login attempts. Please contact the administrator")
                db.session.commit()
                flash("Invalid email or password", "danger")
                return render_template('user/user_login_extends_base.html', form=form)
            
        else:
            flash("Invalid email or password", "danger")
            return render_template('user/user_login_extends_base.html', form = form)
            

    return render_template('user/user_login_extends_base.html', form = form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out!", "success")
    return redirect(url_for('users.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin.index'))
    products = Product.query.filter_by(is_deleted=False).all()
    client_token = gateway.client_token.generate()   
    return render_template('products_extends_base.html', products=products, client_token=client_token)    
    
@bp.route('/transactions')
@login_required
def show_transactions():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template('user/user_transactions.html', transactions=transactions)

@bp.route('/orders')
@login_required
def show_orders():
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
            return redirect(url_for('users.dashboard'))

        amount = float(amount)

        if amount <= 0:
            flash("Amount must be greater than 0.", "danger")
            return redirect(url_for('users.dashboard'))
        
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

            transaction = Transaction(user_id=current_user.id, sum=amount, status="Completed", type = "Deposit")
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

    return redirect(url_for('users.dashboard'))


@bp.route('/cash_out', methods=['POST'])
@login_required
def cash_out():
    try:
        amount = request.form.get('amount')

        if not amount:
            flash("Invalid input. Please try again.", "danger")
            return redirect(url_for('users.dashboard'))

        amount = float(amount)

        if amount <= 0:
            flash("Amount must be greater than 0.", "danger")
            return redirect(url_for('users.dashboard'))

        # Check if user has sufficient balance
        if current_user.balance < amount:
            flash("Insufficient balance to complete the cash out.", "danger")
            return redirect(url_for('users.dashboard'))

        # Deduct amount from user's balance
        current_user.balance -= amount

        transaction = Transaction(user_id=current_user.id, sum=-amount, status="Completed", type = "Cash out")
        db.session.add(transaction)
        db.session.commit()

        flash(f"Successfully cashed out {amount}€ from your balance!", "success")
    except ValueError:
        flash("Invalid amount entered. Please enter a valid number.", "danger")
    except Exception as e:
        print(f"Error during cash_out: {e}")
        flash("An error occurred. Please try again later.", "danger")

    return redirect(url_for('users.dashboard'))

@bp.route('/order_payment/<int:cart_id>', methods=['POST'])
@login_required
def pay_for_order(cart_id):
    try:
        cart = ProductCart.query.get(cart_id)

        if not cart:
            flash("Following user cart was not found.", "danger")
            return redirect(url_for('users.user_dashboard'))

        total_price = sum(item.product.price * item.quantity for item in cart.cart_items)

        if current_user.balance < total_price:
            flash("Insufficient funds. Please add to your balance.", "danger")
            return redirect(url_for('cart.view_cart'))

        # Deduct the price from the user's balance
        current_user.balance -= total_price

        transaction = Transaction(user_id=current_user.id, sum=-total_price, status="Completed", type = "Order payment")
        order = Order(user_id=current_user.id, purchase_price = total_price)
        db.session.add(order)
        db.session.add(transaction)
        db.session.delete(cart)
        db.session.commit()
    
        flash(f"Successfully paid {total_price}€ for your order!", "success")
    except Exception as e:
        print(f"Error during payment: {e}")
        flash("An error occurred. Please try again later.", "danger")

    return redirect(url_for('users.dashboard'))

