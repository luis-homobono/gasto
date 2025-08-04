from sqlalchemy import or_
from flask_login import login_user
from flask import Blueprint, render_template, current_app, redirect, url_for, request

from gasto.models import User
from gasto.extensions import db
from gasto.blueprints.users.forms import LoginForm, RegistrationForm

users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            or_(User.email == form.email.data, User.username == form.email.data)
        ).first()
        if user.check_password(password=form.password.data) and user is not None:
            login_user(user=user)
            # flash('Log in Success!')

            next = request.args.get("next")
            if next == None or next[0] == "/":
                next = url_for("core.index")

            return redirect(next)

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
        return redirect(url_for("users.login"))

    return render_template("users/register.html", form=form)
