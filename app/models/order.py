from app.database import db
from sqlalchemy import func

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    purchase_price = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, default = func.now())

    user = db.relationship("User", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order")