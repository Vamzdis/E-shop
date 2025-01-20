from app.database import db
from datetime import datetime

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    quantity = db.Column(db.Integer, nullable = False)

    product_cart = db.relationship("ProductCart", back_populates = "cart_items")
    product_cart_id = db.relationship("Product", back_populates = "cart_items")
    
    def __init__(self, quantity : int):
        self.quantity = quantity

    def __repr__(self):
        pass
    
