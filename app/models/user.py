from app.database import db
from datetime import datetime
from sqlalchemy import func

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable = False)
    last_name = db.Column(db.String(255), nullable = False)
    login_email = db.Column(db.String(255), unique = True, nullable = False) #adding this already as for the email activation functionality
    password = db.Column(db.String(255), nullable = False)  #only the hashed password should be saved here, should it be with __ for security?
    balance = db.Column(db.Float, default=0, nullable = False)
    is_deleted = db.Column(db.Boolean, default=False, nullable = False)
    is_admin = db.Column(db.Boolean, default=False, nullable = False)
    is_active = db.Column(db.Boolean, default=True, nullable = False)
    failed_login_count = db.Column(db.Integer, default=3)
    block_until = db.Column(db.DateTime, nullable = True)
    created_on = db.Column(db.DateTime, default = func.now())


#I cant thing of a scenario where we would need to specify balance when creating it so I'm not adding it to init method
    def __init__(self, name : str, email : str, password : str, block_until :datetime, created_on : datetime = None):
        self.name = name
        self.email = email
        self.password = password #when does password hashing happen? probably outside the class
        self.block_until = block_until
        self.created_on = created_on


    def __repr__(self):
        return f"{self.name} id ({self.id})"