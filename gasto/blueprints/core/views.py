from flask import Blueprint, render_template, request

core = Blueprint("core", __name__)


@core.route("/")
def index():
    """View for index

    Returns:
        Response: Return a template for index
    """
    return render_template("index.html")
