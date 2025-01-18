from app.database import db
from father import Father
from datetime import datetime

class CartItem(Father):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    quantity = db.Column(db.Integer, nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'))

    def __init__(self, quantity : int, created_on : datetime):
        super().__init__(created_on)
        self.quantity = quantity

    def __repr__(self):
        pass
    
