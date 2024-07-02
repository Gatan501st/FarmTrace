import flask
import flask_login
import flask_moment
import flask_mailman
import flask_sqlalchemy

from config import config

# Set endpoint for the login page
login_manager = flask_login.LoginManager()
login_manager.login_view = "accounts.sign_in"


@login_manager.user_loader
def load_user(user_id):
    # Avoid circular imports
    from .models import User

    # Return logged in user instance
    return User.query.get(int(user_id))


db = flask_sqlalchemy.SQLAlchemy()
mail = flask_mailman.Mail()
moment = flask_moment.Moment()


def create_app(config_name="default"):
    """
    Initialize and configure the Flask application.

    :param config_name: str - The name of the configuration class defined in
        config.py.

    :return app: Flask - The configured Flask application instance.
    """
    app = flask.Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    # Register blueprints for different parts of the application
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .accounts import accounts as accounts_blueprint

    app.register_blueprint(accounts_blueprint, url_prefix="/accounts")

    from .operations import operations as operations_blueprint

    app.register_blueprint(operations_blueprint, url_prefix="/operations")

    return app
