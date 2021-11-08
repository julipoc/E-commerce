from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView, expose


basedir = os.path.abspath(os.path.dirname(__file__))
image_path = os.path.join(basedir, "static/images")
basename = os.path.abspath(image_path)


app = Flask(__name__)

app.config["SECRET_KEY"] = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["FLASK_ADMIN_FLUID_LAYOUT"] = True


db = SQLAlchemy(app)
Migrate(app, db)


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.email == "admin@admin.com":
                return True

    def inaccessible_callback(self, name, **kwargs):
        flash("Please log in as admin!")
        return redirect(url_for("users.login"))

    @expose("/")
    def index(self):
        from project.models import Product
        products = Product.query.all()
        from project.models import User
        users = User.query.all()
        from project.models import Order
        orders = Order.query.all()

        all_products = len(products)
        all_users = len(users)
        all_orders = len(orders)

        data = [
            ("Users", all_users),
            ("Orders", all_orders),
        ]

        labels = [row[0] for row in data]
        values = [row[1] for row in data]

        return self.render("admin/index.html", products=products, users=users, all_products=all_products,
                           all_users=all_users, orders=orders, all_orders=all_orders, data=data, labels=labels,
                           values=values)


admin = Admin(app, index_view=MyAdminIndexView(), template_mode="bootstrap3")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from project.core.views import core
app.register_blueprint(core)

from project.users.views import users
app.register_blueprint(users)

from project.cart.views import carts
app.register_blueprint(carts)
