
from flask import render_template, request, redirect, url_for, Blueprint, current_app, flash
from app.models.product import Product
from app.database import db
from sqlalchemy import func
from app.models.user import User
from werkzeug.utils import secure_filename
from config import Config
import os


admin = Blueprint("admin", __name__, url_prefix = "/admin")


def allowed_file(filename):     
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']   # checks if uploeaded file is in allowed extentions 


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route("/add_product", methods = ["GET", "POST"])
def add_product():
    if request.method == "POST":
        try:
            name = request.form["name"]
            description = request.form["description"]
            price = float(request.form["price"])
            quantity = int(request.form["quantity"])
        except: 
            flash("something went wrong, check input", 'danger')
            return render_template("admin/product_list.html")        #add template
        
        is_available = quantity > 0
        is_deleted = False
        created_on = func.now()
        
        if 'picture' not in request.files:
            flash('there is no file selected','danger')         # reloads the current page if no image is selected
            return redirect(request.url)
        
        picture = request.files["picture"]
 
        if picture.filename == '':
            flash('filename is empty','danger')                  # reloads currnet page if file is not accepted
            return redirect(request.url)

        if picture and allowed_file(picture.filename):
            filename = secure_filename(picture.filename)                                #returns the secure version of the image
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)      #filepath to upload folder
            try:
                picture.save(filepath)                  
            except:
                flash("upload error",'danger')
                return redirect(request.url)
            
        else:
            flash("format not allowed",'danger')
            return redirect(request.url)


        product = Product(
            name=name,
            description=description, 
            price=price, 
            quantity=quantity, 
            is_available=is_available, 
            is_deleted=is_deleted,
            created_on = created_on,
            picture = filename
            )
        
        db.session.add(product)
        db.session.commit()
        flash("product added successfully",'success')
        return redirect(url_for("admin.list_products"))         #add template
    else:
        return render_template("admin/add_product.html")           #add template


@admin.route("/list_products")
def list_products():
    products = Product.query.all()
    return render_template("admin/product_list.html", products=products)    #add template


@admin.route("/delete_product/<int:id>", methods = ["GET", "POST"])
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        flash('Product not found','danger')
        return redirect(request.url)

    if request.method == "POST":
        product.is_deleted = True
        db.session.commit()
        return redirect(url_for("admin.list_products"))         #add template
    else:
        return render_template("admin/product_list.html", product=product)      #add template


@admin.route("/restore_product/<int:id>", methods = ["GET", "POST"])
def restore_product(id):
    product = Product.query.get(id)

    if not product:
        flash('Product not found','danger')
        return redirect(request.url)

    if request.method == "POST":
        product.is_deleted = False
        db.session.commit()
        flash("Product restored successfully", 'success')
        return redirect(url_for("admin.list_products"))         #add template
    else:
        return render_template("admin/product_list.html", product=product)      #add template



@admin.route("/edit_product/<int:id>", methods = ["GET", "POST"])
def edit_product(id):
    product = Product.query.get(id)

    if not product:
        flash("Product not found",'danger')
        return redirect(url_for("admin.list_products"))
    
    if request.method == "POST":
        try:
            product.name = request.form["name"]
            product.description = request.form["description"]
            product.price = request.form["price"]
            product.quantity = request.form["quantity"]

            if 'picture' in request.files and request.files["picture"].filename != '':
                picture = request.files["picture"]
                if allowed_file(picture.filename):
                    filename = secure_filename(picture.filename)                                #returns the secure version of the image
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename) 
                    picture.save(filepath)
                    product.picture=filename
                else:
                    flash("upload error",'danger')
                    return redirect(request.url)
            db.session.commit()
            flash("Entry edited successsfully", "success")      
        except:
            flash("smoething went wrong, check input", 'danger')
            return redirect(request.url) 
        return redirect(url_for("admin.list_products"))    #add url
    else:
        return render_template("admin/edit_product.html", product = product)



@admin.route("/list_users")
def list_users():
    users = User.query.all()
    return render_template("...", users=users)      #add template


@admin.route("/delete_user/<int:id>", methods = ["GET", "POST"])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return "User not found", 404
    
    if request.method == "POST":
        user.is_deleted = True
        db.session.commit()
        return redirect(url_for("..."))             #add template
    else:
        return render_template("...", user = user)  #add template
    

# Administratoriaus galimybės


# Papildyti esamų prekių kiekį

# Peržiūrėti statistika apie prekes. Kiek prekių nupirkta kurią dieną, už kiek nupirkta,
# kurie mėnesiai pelningiausi, kurios prekės geriausiai įvertintos

