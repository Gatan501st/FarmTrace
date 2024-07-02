import os

from flask_migrate import Migrate
from flask_migrate import upgrade

from app import db
from app import create_app
from app.models import Role

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """
    Make application objects available in the Python Flask Interactive Shell
    """
    return dict(db=db)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # Migrate the database to the latest version
    upgrade()

    # Create or update user roles
    Role.insert_roles()
