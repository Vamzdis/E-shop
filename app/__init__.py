from flask import Flask as fl
from flask_login import LoginManager
from config import Config as cfg

from app.models.cart_item import CartItem
from app.models.order_item import OrderItem
from app.models.order import Order
from app.models.product_cart import ProductCart
from app.models.rating import Rating
from app.models.user import User
from app.models.transaction import Transaction

from app.routes import shop_routes
from app.routes.users import user_routes
from app.routes import admin_routes

login_manager = LoginManager() 

def create_app():
    app = fl(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(cfg)

    from app.database import db,migrate
    db.init_app(app)
    migrate.init_app(app,db)

    login_manager.init_app(app)  
    login_manager.login_view = 'user_routes.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(shop_routes.bp)
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(admin_routes.admin)

    return app

app=create_app()
