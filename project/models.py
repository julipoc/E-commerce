from project import db, login_manager, admin
from flask_login import UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_admin.contrib.sqla import ModelView
from flask import url_for, redirect, flash
from flask_admin.menu import MenuLink
from project.admin.forms import AddProductForm, AddOrderForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(124), nullable=False)
    last_name = db.Column(db.String(124), nullable=False)
    email = db.Column(db.String(124), unique=True, nullable=False)
    password_hash = db.Column(db.String(164), nullable=False)
    wishlist = db.relationship("Wishlist", backref="wishlist", lazy=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"User ({self.id}): {self.first_name},{self.last_name}, {self.email}"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(124), nullable=False)
    subcategory = db.Column(db.String(124), nullable=False)
    image = db.Column(db.String(200))
    stock = db.Column(db.Integer, nullable=False, default=1)
    orders = db.relationship("Cart", backref="product", lazy=True)
    wishlist = db.relationship("Wishlist", backref="wishlist product", lazy=True)

    def __repr__(self):
        return f"Product ({self.id}): {self.name}, {self.price}, {self.category} ({self.subcategory}) "


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(124), nullable=False)
    last_name = db.Column(db.String(124), nullable=False)
    email = db.Column(db.String(124), unique=False, nullable=False)
    country = db.Column(db.String(124), nullable=False)
    city = db.Column(db.String(124), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(124), nullable=False)
    card_number = db.Column(db.Integer, nullable=False)
    security_number = db.Column(db.Integer, nullable=False)
    card_date = db.Column(db.String(124), nullable=False)
    items = db.relationship("Cart", backref="order", lazy=True)

    def __repr__(self):
        return f"Order ({self.id}): {self.first_name}, {self.last_name}, {self.city}, {self.card_number}"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))

    def __repr__(self):
        return f"Cart ({self.id}): product id - {self.product_id} , quantity - {self.quantity} "


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    def __repr__(self):
        return f"Wishlist ({self.id}): user id - {self.user_id} , product - {self.product_id} "


class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.email == "admin@admin.com":
                return True

    def inaccessible_callback(self, name, **kwargs):
        flash("Please log in as admin!")
        return redirect(url_for("users.login"))


class MyUserModelView(MyModelView):
    column_searchable_list = ["id", "first_name", "last_name", "email"]
    form_excluded_columns = ("cart", "wishlist")
    column_list = ("first_name", "last_name", "email")


class MyProductModelView(MyModelView):
    column_searchable_list = ["id", "name", "category", "subcategory", "description", "stock", "price"]
    form = AddProductForm


class MyOrderModelView(MyModelView):
    column_searchable_list = ["id", "first_name", "last_name", "email", "address", "country", "city", "card_number"]
    form = AddOrderForm


class MyCartModelView(MyModelView):
    column_searchable_list = ["id", "product_id", "order_id", Product.name, Order.first_name, Order.last_name]
    column_labels = dict(order="Buyer", product="Product")


class MyWishlistModelView(MyModelView):
    column_searchable_list = ["id", "user_id", "product_id", Product.name, User.first_name, User.last_name]


class MainMenuLink(MenuLink):
    def get_url(self):
        return url_for("core.home")


class LogoutLink(MenuLink):
    def get_url(self):
        return url_for("users.logout")


admin.add_view(MyUserModelView(User, db.session, "Users"))
admin.add_view(MyProductModelView(Product, db.session, "Products"))
admin.add_view(MyOrderModelView(Order, db.session, "Buyer Info (orders)"))
admin.add_view(MyCartModelView(Cart, db.session, "Order Info"))
admin.add_view(MyWishlistModelView(Wishlist, db.session, "Users Wishlists"))
admin.add_link(MainMenuLink(name="Jewelry Design"))
admin.add_link(LogoutLink(name="Log Out"))
