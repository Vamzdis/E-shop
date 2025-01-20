#THIS SHOULD NOT BE CUSTOM, THIS SHOULD BE FROM MODELS! It's here just for testing product listing from font-end
class Product():

    def __init__(self, name, description, price, picture, quantity, rating):
        self.name = name
        self.description = description
        self.price = price
        self.picture = picture
        self.quantity = quantity
        self.rating = rating

dummy_products = [
    Product(
        name="Wireless Mouse",
        description="A sleek and responsive wireless mouse.",
        price=29.99,
        picture="https://via.placeholder.com/150?text=Wireless+Mouse",
        quantity=50,
        rating=4.2
    ),
    Product(
        name="Gaming Keyboard",
        description="RGB backlit keyboard with mechanical keys.",
        price=79.99,
        picture="https://via.placeholder.com/150?text=Gaming+Keyboard",
        quantity=30,
        rating=4.8
    ),
    Product(
        name="Noise-Cancelling Headphones",
        description="Premium over-ear headphones with noise cancellation.",
        price=199.99,
        picture="https://via.placeholder.com/150?text=Headphones",
        quantity=20,
        rating=4.6
    ),
    Product(
        name="4K Monitor",
        description="27-inch monitor with stunning 4K UHD resolution.",
        price=399.99,
        picture="https://via.placeholder.com/150?text=4K+Monitor",
        quantity=15,
        rating=4.7
    ),
    Product(
        name="Portable SSD",
        description="1TB portable SSD with fast read/write speeds.",
        price=119.99,
        picture="https://via.placeholder.com/150?text=Portable+SSD",
        quantity=40,
        rating=4.4
    ),
    Product(
        name="Webcam",
        description="1080p HD webcam for video conferencing.",
        price=49.99,
        picture="https://via.placeholder.com/150?text=Webcam",
        quantity=25,
        rating=4.1
    ),
    Product(
        name="Gaming Chair",
        description="Ergonomic gaming chair with adjustable armrests.",
        price=249.99,
        picture="https://via.placeholder.com/150?text=Gaming+Chair",
        quantity=10,
        rating=4.9
    ),
    Product(
        name="Smartphone Stand",
        description="Adjustable aluminum stand for smartphones.",
        price=19.99,
        picture="https://via.placeholder.com/150?text=Smartphone+Stand",
        quantity=100,
        rating=3.9
    ),
    Product(
        name="Bluetooth Speaker",
        description="Portable Bluetooth speaker with deep bass.",
        price=59.99,
        picture="https://via.placeholder.com/150?text=Bluetooth+Speaker",
        quantity=35,
        rating=4.5
    ),
    Product(
        name="USB-C Hub",
        description="Multiport USB-C hub with HDMI and card reader.",
        price=34.99,
        picture="https://via.placeholder.com/150?text=USB-C+Hub",
        quantity=60,
        rating=4.3
    )
]