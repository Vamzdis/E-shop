from app.database import db
from sqlalchemy import func
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    sum = db.Column(db.Float)
    status = db.Column(db.String(255), default = "Pending")
    type = db.Column(db.String(255), default = "Deposit")
    created_on = db.Column(db.DateTime, default = func.now())

    user = db.relationship("User", back_populates="transactions")

    def __init__(self, user_id : int, sum, status:str, type, created_on:datetime=None):
        self.user_id = user_id
        self.sum = sum
        self.status = status
        self.type = type
        self.created_on = created_on