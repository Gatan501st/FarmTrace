from flask import Blueprint
from flask import current_app


operations = Blueprint("operations", __name__)
from . import views, errors


@operations.app_context_processor
def global_variables():
    """
    Provide global variables for templates within the 'operations' blueprint.

    :return: A dictionary containing global variables to inject into templates.
    :rtype: dict

    :params: None
    """
    return dict(
        app_name=current_app.config["ORGANIZATION_NAME"],
    )
