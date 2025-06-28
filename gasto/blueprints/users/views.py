from flask import Blueprint, render_template, current_app

from gasto.blueprints.users.forms import LoginForm

users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print(form.data)

    current_app.logger.info(form.errors)

    return render_template("users/login.html", form=form)
