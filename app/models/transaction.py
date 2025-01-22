from app.database import db
from sqlalchemy import func
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    sum = db.Column(db.Float)
    created_on = db.Column(db.DateTime, default = func.now())

    user = db.relationship("User", back_populates="transactions")

    def __repr__(self):
        pass
    