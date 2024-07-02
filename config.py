import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask security configuration options
    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or "gxvbnmnbvgvghjklmgfdsgacfgvbhnm"
    )

    # SQLAlchemy configuration options
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SLOW_DB_QUERY_TIME = 0.5

    # Application configuration options
    ORGANIZATION_NAME = os.environ.get("ORGANIZATION_NAME") or "Farm Trace"

    # File upload configuration options
    USER_PROFILE_UPLOAD_PATH = os.path.join(
        basedir + "/app/static/images/profiles/users/"
    )

    UPLOAD_EXTENSIONS = [".jpg", ".gif", ".jpeg", ".png"]

    # Mail connection configuration options
    MAIL_BACKEND = "smtp"
    MAIL_SERVER = "smtp.zoho.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_TIMEOUT = None

    # Mail Credentials Settings
    MAIL_DEFAULT_SENDER = "Jisort Ublow Team <info@farmtrace.co.ke>"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "info@farmtrace.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "password")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    JWT_COOKIE_SECURE = True
    JWT_CSRF_CHECK_FORM = False

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEVELOPMENT_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "development.db")


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite://"
    )

    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    JWT_COOKIE_SECURE = True
    JWT_CSRF_CHECK_FORM = True

    SESSION_COOKIE_SECURE = True

    DB_NAME = os.environ.get("DB_NAME") or "chungu_db"
    DB_USERNAME = os.environ.get("DB_USERNAME") or "root"
    DB_HOST = os.environ.get("DB_HOST") or "localhost"
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or "MySQLXXX-123a8910"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("PRODUCTION_DATABASE_URL")
        or f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}"
        + f"/{DB_NAME}"
    )

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # Email errors to the administrators
        # import logging
        # from logging.handlers import SMTPHandler

        # credentials = None
        secure = None
        if getattr(cls, "MAIL_USERNAME", None) is not None:
            # credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, "MAIL_USE_TLS", None):
                secure()

        # TODO: Handling of email sending


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
