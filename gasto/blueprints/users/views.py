from flask import Blueprint, render_template, current_app, redirect, url_for

from gasto.models import User
from gasto.extensions import db
from gasto.blueprints.users.forms import LoginForm, RegistrationForm

users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print(form.data)

    current_app.logger.info(form.errors)

    return render_template("users/login.html", form=form)


@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        user.firstname = form.firstname.data or ""
        user.lastname = form.lastname.data or ""

        db.session.add(user)
        db.session.commit()

        current_app.logger.info("User Registered Successfully")
        return redirect(url_for('core.index'))

    return render_template("users/register.html", form=form)
