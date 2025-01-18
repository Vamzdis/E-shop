from flask import Flask as fl, render_template
import config as cfg

#making a note that routes will have to be imported here and blueprints will need to be setup
# from app.routes import route file

def create_app():
    app = fl(__name__, static_folder='templates/static')
    app.config.from_object(cfg)

    from app.database import db,migrate
    db.init_app(app)
    migrate.init_app(app,db)

    #after route import this will be something like
    # app.register_blueprint(route file.bp)
    app.register_blueprint()

    return app

app=create_app()