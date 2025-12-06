from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import date, datetime

from models.emprestimos import Emprestimo
from models.users import User
from models.itens import Item
from app import db

emprestimo_bp = Blueprint("emprestimo", __name__, url_prefix="/emprestimos", template_folder="templates/emprestimos")

@emprestimo_bp.route("/")
@login_required
def listar():
    emprestimos = Emprestimo.all()
    return render_template("emprestimos/emprestimos.html", emprestimos=emprestimos, User=User,Item=Item)

@emprestimo_bp.route("/adicionar", methods=["POST"])
@login_required
def adicionar():
    item_id = request.form.get("item_id")
    
    if not item_id:
        flash("Item inválido.", "error")
        return redirect(url_for("item.itens"))

    item = Item.get(int(item_id))

    if not item or item.quantidade <= 0:
        flash("Item indisponível.", "error")
        return redirect(url_for("item.itens"))

    emprestimo = Emprestimo(
        user_id=current_user.id,
        item_id=item_id,
        data_emprestimo=date.today(),
        status="pendente"
    )
    emprestimo.save()

    item.update(quantidade=item.quantidade - 1)

    flash("Empréstimo registrado com sucesso!", "success")
    return redirect(url_for("emprestimo.listar"))


@emprestimo_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    emprestimo = Emprestimo.get(id)
    usuarios = User.all()
    itens = Item.all()

    if not emprestimo:
        flash("Empréstimo não encontrado!", "error")
        return redirect(url_for("emprestimo.listar"))

    if request.method == "POST":
        try:
            user_id = request.form.get("usuario_id")
            item_id = request.form.get("item_id")
            status = request.form.get("status") or "pendente"
            data_devolucao = request.form.get("data_devolucao") or None

            emprestimo.update(
                user_id=user_id,
                item_id=item_id,
                status=status,
                data_devolucao=data_devolucao
            )

            flash("Empréstimo atualizado com sucesso!", "success")
            return redirect(url_for("emprestimo.listar"))

        except Exception:
            db.session.rollback()
            flash("Erro ao atualizar empréstimo.", "error")
            return redirect(url_for("emprestimo.editar", id=id))

    return render_template("emprestimos/editar.html", emprestimo=emprestimo, usuarios=usuarios, itens=itens)

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
        data_devolucao=date.today()
    )

    item.update(quantidade=item.quantidade + 1)

    flash("Item devolvido com sucesso!", "success")
    return redirect(url_for("emprestimo.listar"))


@emprestimo_bp.route("/remover/<int:id>", methods=["POST"])
@login_required
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