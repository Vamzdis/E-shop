import os
from big_secrets import SQLALCHEMY_DATABASE_URI, SECRET_KEY
 
class Config:
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SECRET_KEY = SECRET_KEY
 

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))     
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
 
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)