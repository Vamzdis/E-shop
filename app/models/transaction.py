from app.database import db
from app.models.father import Father

class Transaction(Father):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    sum = db.Column(db.Float)

    user = db.relationship("User", back_populates="transactions")

    def __init__(self, sum):
        self.sum = sum

    def __repr__(self):
        pass
    