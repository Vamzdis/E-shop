from app.database import db
from sqlalchemy import func

class ProductCart(db.Model):
    __tablename__ = 'product_carts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    created_on = db.Column(db.DateTime, default = func.now())

    user = db.relationship('User', back_populates='products_carts')
    cart_items = db.relationship('CartItem', back_populates='products_carts', cascade="all, delete")