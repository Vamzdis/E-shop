import sys
import os
 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 
from app import create_app
from app.models.product import Product
from app.database import db
from faker import Faker
import random
from datetime import datetime
 
app = create_app()
UPLOADS_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'app', 'static', 'uploads')
image_files = [f for f in os.listdir(UPLOADS_FOLDER) if f.endswith('.png')]

fake = Faker()

def generate_description():
    words = fake.words(nb=random.randint(3, 50))  
    description = " ".join(words).capitalize()
   
 
    if len(description) > 255:
        description = description[:252] + "..."  
   
    return description
 
def create_fake_products(count=30):
    with app.app_context():  
        for _ in range(count):
            product = Product(
                name=" ".join(fake.words(nb=random.randint(1, 5))).capitalize(),
                description=generate_description(),
                price=round(fake.random_number(digits=2), 2),
                picture=random.choice(image_files),
                quantity=random.randint(1, 200),
                is_available=True,
                is_deleted=False,
                created_on=fake.date_time_between(start_date="-1y", end_date="now"),
                rating=round(random.uniform(1.0, 5.0), 1)
            )
            db.session.add(product)
        db.session.commit()
        print(f"{count} produktai sukurti sėkmingai.")
 
def generate_fake_data():
    create_fake_products(30)
    print("Netikri duomenys sugeneruoti sėkmingai.")
 
if __name__ == "__main__":
    generate_fake_data()