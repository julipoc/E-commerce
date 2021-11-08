from project import db
from flask import Blueprint, flash, redirect, render_template, url_for, session
from project.users.forms import RegistrationForm, LoginForm
from project.models import User, Product, Wishlist
from flask_login import logout_user, login_user, login_required, current_user

users = Blueprint("users", __name__)


@users.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in!")
        return redirect(url_for("users.login"))
    return render_template("registration.html", form=form, total_quantity=session["total_quantity"])


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("core.home", user=user))
    return render_template("login.html", form=form, total_quantity=session["total_quantity"])


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("core.home"))


@users.route("/account")
@login_required
def account():
    wishlist = Wishlist.query.filter_by(user_id=current_user.id).all()
    products = []

    for wish in wishlist:
        product = Product.query.filter_by(id=wish.product_id).first()
        products.append(product)
    return render_template("account.html", wishlist=wishlist, products=products, total_quantity=session["total_quantity"])


@users.route("/<product_id>/add-to-wishlist")
@login_required
def add_to_wishlist(product_id):
    wishlist = Wishlist(user_id=current_user.id, product_id=product_id)
    db.session.add(wishlist)
    db.session.commit()
    return redirect(url_for("users.account"))


@users.route("/<product_id>/remove-from-wishlist")
@login_required
def remove_from_wishlist(product_id):
    wishlist = Wishlist.query.filter_by(product_id=product_id).first()
    db.session.delete(wishlist)
    db.session.commit()
    return redirect(url_for("users.account"))
