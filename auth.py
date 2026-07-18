from flask import Blueprint, render_template, request, redirect, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from forms import LoginForm, RegisterForm

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/dashboard")

    form = LoginForm()

    if form.validate_on_submit(): 
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.hashed_password, form.password.data):
            login_user(user)
            return redirect("/dashboard")

        form.password.errors.append("Invalid username or password")

    return render_template("login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    
    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            form.username.errors.append("Username already in use")
        else:
            user = User(username=form.username.data, hashed_password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect("/dashboard")

    return render_template("register.html",form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
