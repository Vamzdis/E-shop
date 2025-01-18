from app.database import db
from sqlalchemy.sql import func


class Father(db.Model):
    created_on = db.Column(db.DateTime, default = func.now())
    