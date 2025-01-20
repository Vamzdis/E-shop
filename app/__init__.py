from flask import Flask as fl
import config as cfg

from app.models.cart_item import CartItem
from app.models.order_item import Order_items
from app.models.order import Order
from app.models.product_cart import ProductCart
from app.models.rating import Rating
from app.models.user import User
from app.models.transaction import Transaction

from app.routes import shop_routes


def create_app():
    app = fl(__name__, static_folder='templates/static')
    app.config.from_object(cfg)

    from app.database import db,migrate
    db.init_app(app)
    migrate.init_app(app,db)

    # app.register_blueprint(shop_routes.bp)
    # app.register_blueprint()

    return app

app=create_app()