from flask_login import login_required
from flask import Blueprint, render_template, request, redirect, url_for


core = Blueprint("core", __name__)


@core.route("/")
@login_required
def index():
    """View for index

    Returns:
        Response: Return a template for index
    """
    return render_template("index.html")
