from app.database import db

class OrderItem(db.Model):
    __tablename__ = 'orders_items'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer, nullable = False)

    order = db.relationship("Order", back_populates="order_items")
    product = db.relationship("Product", back_populates="order_items")