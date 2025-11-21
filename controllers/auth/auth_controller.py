from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.users import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.senha_hash, senha):
            login_user(user)
            flash("Login realizado!", "success")
            return redirect(url_for("home"))
        else:
            flash("Email ou Senha incorretos. Tente novamente.", "error")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        if User.query.filter_by(email=email).first():
            flash("Email já está em uso.", "error")
            return redirect(url_for("auth.register"))

        user = User(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha)
        )

        user.save()
        flash("Conta criada!", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))