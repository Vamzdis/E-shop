from app.database import db
from app.models.father import Father

class ProductCart(Father):
    __tablename__ = 'products_carts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    user = db.relationship("User", back_populates="product_carts")
    cart_items = db.relationship("CartItem", back_populates="product_carts")

    def __init__(self, created_on):
        super().__init__(created_on)
        
    def __repr__(self):
        pass


