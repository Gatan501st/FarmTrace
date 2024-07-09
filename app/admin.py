from flask import redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from .models import db, User, Role, Product, Retailer,\
    Wholesaler, Farmer, Manufacturer, Administrator, Item,\
    Batch

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_title == 'Administrator'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('accounts.sign_in'))

def setup_admin(app):
    admin = Admin(app, name='Farm Trace Admin', template_mode='bootstrap3')
    admin.add_view(MyModelView(User, db.session, "Users"))
    admin.add_view(MyModelView(Role, db.session, "Roles"))
    admin.add_view(MyModelView(Product, db.session, 'Products'))
    admin.add_view(MyModelView(Batch, db.session, "Batches"))