from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import date, datetime, timezone

from decorators import admin_required
from models.emprestimos import Emprestimo
from models.users import User
from models.itens import Item
from storage import db

emprestimo_bp = Blueprint("emprestimo", __name__, url_prefix="/emprestimos", template_folder="templates/emprestimos")

@emprestimo_bp.route("/")
@login_required
def listar():

    if current_user.is_admin():
        emprestimos = Emprestimo.all()
    else:
        emprestimos = Emprestimo.query.filter_by(user_id =current_user.id).all()

    return render_template("emprestimos/emprestimos.html", emprestimos=emprestimos, User=User,Item=Item)

@emprestimo_bp.route("/adicionar", methods=["POST"])
@login_required
def adicionar():
    LIMITE_EMPRESTIMOS = 3

    item_id = request.form.get("item_id")

    if not item_id:
        flash("Item inválido.", "error")
        return redirect(url_for("item.itens"))    

    total_ativos = Emprestimo.ativos_por_usuario(current_user.id)

    if total_ativos >= LIMITE_EMPRESTIMOS:
        flash(f"Você atingiu o limite de {LIMITE_EMPRESTIMOS} empréstimos ativos.","error") 
        return redirect(url_for("item.itens"))

    item = Item.get(int(item_id))

    if not item or item.quantidade <= 0:
        flash("Item indisponível.", "error")
        return redirect(url_for("item.itens"))

    emprestimo = Emprestimo(
        user_id=current_user.id,
        item_id=item_id,
        status="pendente"
    )
    emprestimo.save()

    item.update(quantidade=item.quantidade - 1)

    flash("Empréstimo registrado com sucesso!", "success")
    return redirect(url_for("emprestimo.listar"))

@emprestimo_bp.route("/devolver/<int:id>", methods=["POST"])
@login_required
def devolver(id):
    emp = Emprestimo.get(id)
    if not emp:
        flash("Empréstimo não encontrado.", "error")
        return redirect(url_for("emprestimo.listar"))

    if emp.user_id != current_user.id:
        flash("Você não pode devolver um empréstimo de outro usuário!", "error")
        return redirect(url_for("emprestimo.listar"))

    item = Item.get(emp.item_id)
    if not item:
        flash("Item associado não encontrado!", "error")
        return redirect(url_for("emprestimo.listar"))

    emp.update(
        status="devolvido",
        data_devolucao=datetime.now()
    )

    item.update(quantidade=item.quantidade + 1)

    flash("Item devolvido com sucesso!", "success")
    return redirect(url_for("emprestimo.listar"))


@emprestimo_bp.route("/remover/<int:id>", methods=["POST"])
@admin_required
def remover(id):
    emprestimo = Emprestimo.get(id)
    if not emprestimo:
        flash("Empréstimo não encontrado.", "error")
        return redirect(url_for("emprestimo.listar"))

    try:
        emprestimo.delete()
        flash("Empréstimo removido com sucesso!", "success")

    except Exception:
        db.session.rollback()
        flash("Erro ao remover empréstimo.", "error")

    return redirect(url_for("emprestimo.listar"))