from flask import session, request
from flask import Flask
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_moment import Moment
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import config

# Set endpoint for the login page
login_manager = LoginManager()
login_manager.login_view = "accounts.sign_in"


@login_manager.user_loader
def load_user(user_id):
    from .models import User

    return User.query.get(user_id)


db = SQLAlchemy()
mail = Mail()
moment = Moment()
migrate = Migrate()


def create_app(config_name="default"):
    """
    Initialize and configure the Flask application.

    :param config_name: str - The name of the configuration class defined in
        config.py.

    :return app: Flask - The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)

    from app.models import User, Role
    from app.admin import setup_admin

    setup_admin(app)

    # Register blueprints for different parts of the application
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .accounts import accounts as accounts_blueprint

    app.register_blueprint(accounts_blueprint, url_prefix="/accounts")

    from .listings import listings as listings_blueprint

    app.register_blueprint(listings_blueprint, url_prefix="/listings")

    from .products import products as products_blueprint

    app.register_blueprint(products_blueprint, url_prefix="/products")

    from .orders import orders as orders_blueprint

    app.register_blueprint(orders_blueprint, url_prefix='/orders')

    from .shipments import shipments as shipments_blueprint

    app.register_blueprint(shipments_blueprint, url_prefix='/shipments')

    return app
