from app.database import db
from father import Father

class Product(Father):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    is_available = db.Column(db.Boolean, default = False, nullable = False)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False)


    def __init__(self, name, description, price, is_available, is_deleted, quantity, created_on):
        super().__init__(created_on)
        self.name = name
        self.description = description
        self.price = price
        self.is_available = is_available
        self.is_deleted = is_deleted
        self.quantity = quantity

    def __repr__(self):
        return f" Product: {self.name}, price - {self.price}, description - {self.description}"


