from flask import current_app
from app.models import Listing
import os

from flask_migrate import Migrate
from flask_migrate import upgrade

from app import db
from app import create_app
from app.models import Role

config_name = os.getenv("FLASK_CONFIG") or "default"
app = create_app(config_name)
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


if __name__ == '__main__':
    with app.app_context():
        Role.insert_roles()
        host = app.config['HOST']
        port = app.config['PORT']

    app.run(
        host=host,
        port=5500,
        debug=True,
        use_reloader=True
    )
