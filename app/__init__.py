from flask import Flask as fl
from config import Config as cfg

from app.models.cart_item import CartItem
from app.models.order_item import Order_items
from app.models.order import Order
from app.models.product_cart import ProductCart
from app.models.rating import Rating
from app.models.user import User
from app.models.transaction import Transaction

from app.routes import shop_routes
from app.routes.users import user_routes
from app.routes import admin_routes

def create_app():
    app = fl(__name__, static_folder='static')
    app.config.from_object(cfg)

    from app.database import db,migrate
    db.init_app(app)
    migrate.init_app(app,db)

    app.register_blueprint(shop_routes.bp)
    app.register_blueprint(user_routes.user_routes)
    app.register_blueprint(admin_routes.admin)

    return app

app=create_app()