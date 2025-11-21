from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from models.users import User

user_bp = Blueprint("user", __name__, url_prefix="/users", template_folder="templates/users")

@user_bp.route("/")
@login_required
def listar():
    usuarios = User.all()
    return render_template("users/usuarios.html", usuarios=usuarios)

@user_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    u = User.get(id)

    if not u:
        flash("Usuário não encontrado!", "error")
        return redirect(url_for("user.listar"))

    if request.method == "POST":

        try:
            u.update(
                nome=request.form.get("nome"),
                cpf=request.form.get("cpf"),
                email=request.form.get("email"),
                senha=request.form.get("senha") 
            )
            flash("Usuário atualizado com sucesso!", "success")
        except:
            flash("Erro ao atualizar usuário.", "error")

        return redirect(url_for("user.listar"))

    return render_template("users/editar.html", user=u)

@user_bp.route("/deletar/<int:id>", methods=["POST"])
@login_required
def deletar(id):

    try:
        if User.delete(id):
            flash("Usuário removido com sucesso!", "success")
        else:
            flash("Usuário não encontrado.", "error")

    except:
        flash("Não foi possível remover o usuário.", "error")

    return redirect(url_for("user.listar"))