from flask import Flask as fl
import config as cfg

from app.routes import shop_routes

def create_app():
    app = fl(__name__, static_folder='templates/static')
    app.config.from_object(cfg)

    from app.database import db,migrate
    db.init_app(app)
    migrate.init_app(app,db)

    app.register_blueprint(shop_routes.bp)

    return app

app=create_app()