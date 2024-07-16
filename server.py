from flask import current_app, request, session, abort
from app.models import Listing
import os
import uuid

from flask_migrate import Migrate
from flask_migrate import upgrade

from app import db
from app import create_app
from app.models import Role

config_name = os.getenv("FLASK_CONFIG") or "default"
app = create_app(config_name)
migrate = Migrate(app, db)


@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        req_token = request.form.get('_csrf_token', None)
        if req_token is None:
            req_token = request.headers.get('X-CSRFToken')
        if not token or token != req_token:
            abort(403)
        session['_csrf_token'] = token


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(uuid.uuid4())
    return session['_csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token


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
        port=port,
        debug=True,
        use_reloader=True
    )
