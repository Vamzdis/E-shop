from app.database import db
from app.models.father import Father
from datetime import datetime



class Order_items(Father):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer, nullable = False)

    order = db.relationship("Order", back_populated="order_items")
    product = db.relationship("Product", back_populates="order_items")


    def __init__(self, id : int, user_id : int, purchase_price : float, created_on : datetime):
        super().__init__(created_on)
        self.id = id
        self.user_id = user_id
        self.purchase_price = purchase_price
        self.created_on = created_on


    def __repr__(self):
        pass