from app.database import db
from app.models.father import Father

class Rating(Father):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.foreign_key("products.id"))
    user_id = db.Column(db.Integer, db.foreign_key("users.id"))
    rating = db.Column(db.Float)

    product = db.relationship("Product", back_populates = "ratings")
    user = db.relationship("User", back_populates = "ratings")

    def __init__(self, rating):
        self.rating = rating

    def __repr__(self):
        pass

                           