from app.database import db
from datetime import datetime

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    products_cart_id = db.Column(db.Integer, db.ForeignKey('product_carts.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable = False)

    product_carts = db.relationship('ProductCart', back_populates='cart_items')
    product = db.relationship('Product', back_populates='cart_items')
    
    def __init__(self, quantity : int, created_on : datetime):
        self.quantity = quantity
        self.created_on = created_on

    def __repr__(self):
        pass
    
