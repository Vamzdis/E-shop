from app.database import db
from sqlalchemy import func

class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    created_on = db.Column(db.DateTime, default = func.now())

    def __init__(self, created_on=None):
        self.created_on = created_on
        
    def __repr__(self):
        pass


