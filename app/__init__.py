from flask import Flask as fl
from config import Config as cfg

from app.routes import shop_routes
from app.routes.users import user_routes

def create_app():
    app = fl(__name__, static_folder='static')
    app.config.from_object(cfg)

    from app.database import db,migrate
    db.init_app(app)
    migrate.init_app(app,db)

    app.register_blueprint(shop_routes.bp)
    app.register_blueprint(user_routes.bp)

    return app

app=create_app()