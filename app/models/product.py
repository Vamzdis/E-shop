from app.database import db
from sqlalchemy import func

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    picture = db.Column(db.String(255), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    rating = db.Column(db.Float, nullable = True)
    is_available = db.Column(db.Boolean, default = False, nullable = False)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False)
    created_on = db.Column(db.DateTime, default = func.now())

    cart_items = db.relationship("CartItem", back_populates="product")
    order_items = db.relationship("OrderItem", back_populates="product")
    rating = db.relationship("Rating",back_populates="product")


    def __init__(self, name, description, price, picture, quantity, created_on=None):
        self.name = name
        self.description = description
        self.price = price
        self.picture = picture
        self.quantity = quantity
        self.created_on = created_on

    def __repr__(self):
        return f" Product: {self.name}, price - {self.price}, description - {self.description}"


