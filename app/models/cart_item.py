from app.database import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    quantity = db.Column(db.Integer, nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'))

    def __init__(self, quantity : int):
        self.quantity = quantity

    def __repr__(self):
        pass
    
