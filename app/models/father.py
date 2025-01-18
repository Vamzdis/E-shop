from app.database import db
from sqlalchemy.sql import func


class Father(db.Model):
    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    created_on = db.Column(db.DateTime, default = func.now())
    