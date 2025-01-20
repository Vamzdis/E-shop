from flask import Blueprint, render_template, request, redirect, url_for
# from flask import request, redirect, url_for #very likely will need these in the nearby future

from app.database import db

from app.models.product import Product
from app.models.dummies import dummy_products

bp = Blueprint('shop', __name__)

@bp.route('/')
def show():

    products = dummy_products

    return render_template("products_extends_base.html", products=products)