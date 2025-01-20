from app.database import db
from app.models.father import Father
from datetime import datetime



class Order(Father):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    purchase_price = db.Column(db.Float, nullable=False)

    user = db.relationship("User", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order")


    def __init__(self, id : int, user_id : int, purchase_price : float, created_on: datetime):
        super().__init__(created_on)
        self.id = id
        self.user_id = user_id
        self.purchase_price = purchase_price
        self.created_on = created_on 

    def __repr__(self):
        pass
