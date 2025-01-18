from app.database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255)) #adding this already as for the email activation functionality
    password = db.Column(db.String(255), nullable = False)  #only the hashed password should be saved here, should it be with __ for security?
    balance = db.Column(db.Float, default=0, nullable = False)
    is_deleted = db.Column(db.Boolean, default=False, nullable = False)

#I cant thing of a scenario where we would need to specify balance when creating it so I'm not adding it to init method
    def __init__(self, name : str, email : str, password : str):
        super().__init__() #in the examples we did I remember mixed opinions if this should be kept on not so I'm keeping it just in case
        self.name = name
        self.email = email
        self.password = password #when does password hashing happen? probably outside the class

    def __repr__(self):
        return f"{self.name} id ({self.id})"