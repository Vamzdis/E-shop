from flask import Blueprint, render_template
from flask_login import current_user
from sqlalchemy import func

from app.database import db

from app.models.product import Product
from app.models.user import User
from app.models.rating import Rating

bp = Blueprint('shop', __name__)

@bp.route('/')
def show():
    products_query = db.session.query(
        Product.id,
        Product.name,
        Product.description,
        Product.price,
        Product.picture,
        Product.quantity,
        Product.is_deleted,
        func.coalesce(func.avg(Rating.rating), 0).label('average_rating'),
        func.count(Rating.id).label('total_ratings')
    ).outerjoin(Rating, Rating.product_id == Product.id) \
     .group_by(Product.id)
    
    if current_user.is_authenticated and current_user.is_admin:
        products = products_query.filter_by(Product.is_deleted==False).all()  

    else:
    #using filter here because you cant use quantity comparisons in filter by
        products = products_query.filter(Product.is_deleted == False, Product.quantity > 0 ).all()


    return render_template("products_extends_base.html", products=products)
  

@bp.route("/product/<int:id>")
def view_product(id):
    product = Product.query.get(id)
    ratings = (
        db.session.query(Rating, User.name)
        .join(User, User.id == Rating.user_id)
        .filter(Rating.product_id == id)
        .all()
    )
    total_ratings = db.session.query(func.count(Rating.id)).filter_by(product_id=id).scalar()
    average_rating = db.session.query(func.avg(Rating.rating)).filter_by(product_id=id).scalar()
    return render_template('user/view_product.html', product=product, ratings=ratings, total_ratings=total_ratings, average_rating=round(average_rating, 1) if average_rating else 0)
