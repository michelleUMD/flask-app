from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import RegistrationForm, LoginForm, UpdatePasswordForm
from ..models import User

users = Blueprint('users', __name__, static_folder='static', template_folder='templates')


""" ************ User Management views ************ """


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("packages.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("packages.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("users.account"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("packages.index"))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    password_form = UpdatePasswordForm()

    if password_form.validate_on_submit():
        # current_user.username = username_form.username.data
        
        hashed = bcrypt.generate_password_hash(password_form.password.data).decode("utf-8")
        current_user.modify(password=hashed)
        current_user.save()

        flash("Successfully changed password")

        return redirect(url_for("users.account"))

    return render_template(
        "account.html",
        title="Account",
        password_form=password_form,
    )
