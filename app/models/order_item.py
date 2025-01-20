from app.database import db

class Order_items(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer, nullable = False)

    order = db.relationship("Order", back_populated="order_items")
    product = db.relationship("Product", back_populates="order_items")


    def __init__(self, id : int, user_id : int, purchase_price : float):
        self.id = id
        self.user_id = user_id
        self.purchase_price = purchase_price



    def __repr__(self):
        pass