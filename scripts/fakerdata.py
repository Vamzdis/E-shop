import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from faker import Faker
from werkzeug.security import generate_password_hash
from app.database import db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.rating import Rating
from app.models.product_cart import ProductCart
from app.models.cart_item import CartItem
from app.models.transaction import Transaction
from datetime import datetime
from app import create_app

app = create_app()
fake = Faker()

UPLOADS_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'app', 'static', 'uploads')
image_files = [f for f in os.listdir(UPLOADS_FOLDER) if f.endswith('.png')]

def generate_description():
    words = fake.words(nb=random.randint(3, 50))  
    description = " ".join(words).capitalize()  
    return description[:252] + "..." if len(description) > 255 else description

with app.app_context():
    def create_admin_user():
        admin = User(
            name="Admin",
            last_name="Administrator",
            login_email="admin@admin.com",
            password=generate_password_hash("123"),
            is_admin=True,
            is_active=True,
            is_deleted=False,
            balance=0.0,
            created_on=datetime.now()
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin was created")

    def create_fake_users(count=10):
        for _ in range(count):
            user = User(
                name=fake.first_name(),
                last_name=fake.last_name(),
                login_email=fake.unique.email(),
                password=generate_password_hash(fake.password()),
                balance=round(random.uniform(0, 1000), 2),
                is_deleted=False,
                is_admin=False,
                is_active=True,
                created_on=fake.date_time_between(start_date="-2y", end_date="now")
            )
            db.session.add(user)
        db.session.commit()
        print(f"{count} fake users created")

    def create_fake_products(count=30):
        for _ in range(count):
            product = Product(
                name=" ".join(fake.words(nb=random.randint(1, 5))).capitalize(),
                description=generate_description(),
                price=round(random.uniform(5, 500), 2),
                picture=random.choice(image_files),
                quantity=random.randint(1, 200),
                is_available=True,
                is_deleted=False,
                created_on=fake.date_time_between(start_date="-1y", end_date="now"),
                rating=round(random.uniform(1.0, 5.0), 1)
            )
            db.session.add(product)
        db.session.commit()
        print(f"{count} products created")

    def create_fake_orders(count=10):
        users = User.query.all()
        products = Product.query.all()
        for _ in range(count):
            user = random.choice(users)
            order = Order(
                user_id=user.id,
                purchase_price=round(random.uniform(50, 500), 2),
                created_on=fake.date_time_between(start_date="-1y", end_date="now")
            )
            db.session.add(order)
            db.session.commit()

            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=random.randint(1, 10)
                )
                db.session.add(order_item)
        db.session.commit()
        print(f"{count} fake orders created")

    def create_fake_carts(count=10):
        users = User.query.all()
        products = Product.query.all()
        for _ in range(count):
            user = random.choice(users)
            cart = ProductCart(
                user_id=user.id,
                created_on=fake.date_time_between(start_date="-6m", end_date="now")
            )
            db.session.add(cart)
            db.session.commit()

            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                cart_item = CartItem(
                    products_cart_id=cart.id,
                    product_id=product.id,
                    quantity=random.randint(1, 5)
                )
                db.session.add(cart_item)
        db.session.commit()
        print(f"{count} fake carts created")
    
    def create_fake_ratings(count=30):
        users = User.query.all()
        products = Product.query.all()
        for _ in range(count):
            rating = Rating(
                product_id=random.choice(products).id,
                user_id=random.choice(users).id,
                rating=round(random.uniform(1.0, 5.0), 1),
                created_on=fake.date_time_between(start_date="-1y", end_date="now")
            )
            db.session.add(rating)
        db.session.commit()
        print(f"{count} Fake ratings")

    def create_fake_transactions(count=50):
        users = User.query.all()

        for _ in range(count):
            transaction = Transaction(
                user_id=random.choice(users).id,
                sum=round(random.uniform(10.0, 1000.0), 2),  # Generuojama atsitiktinė suma
                created_on=fake.date_time_between(start_date="-1y", end_date="now")
            )
            db.session.add(transaction)
        db.session.commit()
        print(f"{count} transaction created")

    def generate_fake_data():
        create_admin_user()
        create_fake_users(10)
        create_fake_products(20)
        create_fake_orders(10)
        create_fake_carts(10)
        create_fake_ratings(30)
        create_fake_transactions(20)
        print("Done")

    generate_fake_data()









