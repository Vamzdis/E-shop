from app.database import db
from sqlalchemy import func

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.foreign_key("products.id"))
    user_id = db.Column(db.Integer, db.foreign_key("users.id"))
    rating = db.Column(db.Float)
    created_on = db.Column(db.DateTime, default = func.now())

    product = db.relationship("Product", back_populates = "ratings")
    user = db.relationship("User", back_populates = "ratings")

    def __init__(self, rating, created_on=None):
        self.rating = rating
        self.created_on = created_on

    def __repr__(self):
        pass

                           