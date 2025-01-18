from app.database import db
from father import Father

class Cart(Father):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __init__(self, created_on):
        super().__init__(created_on)
        
    def __repr__(self):
        pass


