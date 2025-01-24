from flask import Blueprint, render_template, flash, request, redirect,url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from app.database import db

from app.models.product import Product
from app.models.user import User
from app.models.rating import Rating

bp = Blueprint('shop', __name__)

@bp.route('/')
def show():
     # Sukuriam objektą, kad galėtume panaudoti average rating iš reitingų lentelės ir atvaizduoti jį prie produktų sąrašo
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
        products = products_query.filter(Product.is_deleted==False).all()  

    else:
    #using filter here because you cant use quantity comparisons in filter by
        products = products_query.filter(Product.is_deleted == False, Product.quantity > 0 ).all()


    return render_template("products_extends_base.html", products=products)
  

@bp.route("/product/<int:id>")
def view_product(id):
    product = Product.query.get_or_404(id)

    # Tikrinam ar vartotojas jau vertino šitą produktą (tinkamo mygtuko atvaizdavimui)
    user_rating = None
    if current_user.is_authenticated:
        user_rating = Rating.query.filter_by(user_id=current_user.id, product_id=id).first()

    # Gaunam visus reitingus su vartotojų vardais
    ratings = (
        db.session.query(Rating, User.name)
        .join(User, User.id == Rating.user_id)
        .filter(Rating.product_id == id)
        .all()
    )
    # Apskaičiuojam bendrą įvertinimų skaičių ir išvedam vidurkį
    total_ratings = db.session.query(func.count(Rating.id)).filter_by(product_id=id).scalar()
    average_rating = db.session.query(func.avg(Rating.rating)).filter_by(product_id=id).scalar()
    return render_template('user/view_product.html', product=product, ratings=ratings, total_ratings=total_ratings, average_rating=round(average_rating, 1) if average_rating else 0)

@bp.route('/rate_product/<int:id>', methods=['POST'])
@login_required
def rate_product(id):
    rating_value = int(request.form.get('rating'))

    # Patikrinam ar vartotojas jau vertino šį produktą
    rating = Rating.query.filter_by(product_id=id, user_id=current_user.id).first()

    # Atnaujinam arba sukuriam naują įvertinimą
    if rating:
        rating.rating = rating_value
        flash("Rating updated!", "success")
    else:
        new_rating = Rating(product_id=id, user_id=current_user.id, rating=rating_value)
        db.session.add(new_rating)
        flash("Rating submitted!", "success")

    db.session.commit()
    return redirect(url_for('shop.view_product', id=id))

@bp.route('/remove_rating/<int:id>', methods=['POST'])
@login_required
def remove_rating(id):
    # Patikrinam ar vartotojas jau vertino šį produktą
    rating = Rating.query.filter_by(product_id=id, user_id=current_user.id).first()

    # Ištrinam produkto įvertnima
    if rating:
        db.session.delete(rating)
        db.session.commit()
        flash('Rating removed successfully.', 'success')
    else:
        flash('No rating found.', 'danger')

    return redirect(url_for('shop.view_product', id=id))
