from app.database import db
from app.models.father import Father
from datetime import datetime

class CartItem(Father):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    quantity = db.Column(db.Integer, nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_cart_id = db.Column(db.Integer, db.ForeignKey('product_cart.id'))

    product_cart = db.relationship("ProductCart", back_populates = "cart_items")
    product_cart_id = db.relationship("Product", back_populates = "cart_items")
    
    def __init__(self, quantity : int, created_on : datetime):
        super().__init__(created_on)
        self.quantity = quantity

    def __repr__(self):
        pass
    
