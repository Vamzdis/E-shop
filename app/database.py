from flask_sqlalchemy import SQLAlchemy as sqla
from flask_migrate import Migrate

db = sqla()
migrate = Migrate()