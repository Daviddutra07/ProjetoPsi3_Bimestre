from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
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

@emprestimo_bp.route("/adicionar", methods=["GET", "POST"])
@login_required
def adicionar():
    usuarios = User.all()
    itens = Item.all()
    hoje = date.today().isoformat()

    if request.method == "POST":
        try:
            user_id = request.form.get("usuario_id")
            item_id = request.form.get("item_id")
            if not user_id or not item_id:
                flash("Preencha todos os campos obrigatórios!", "error")
                return redirect(url_for("emprestimo.adicionar"))


            item = Item.get(int(item_id))
            if not item or item.quantidade <= 0:
                flash("Este item não está disponível.", "error")
                return redirect(url_for("emprestimo.adicionar"))

            emprestimo = Emprestimo(
                user_id=user_id,
                item_id=item_id,
                data_emprestimo=hoje,
                data_devolucao=None,
                status="pendente"
            )
            emprestimo.save()

            # atualizar estoque (-1)
            item.quantidade -= 1
            item.save()

            flash("Empréstimo registrado com sucesso!", "success")
            return redirect(url_for("emprestimo.listar"))

        except Exception:
            db.session.rollback()
            flash("Ocorreu um erro ao registrar o empréstimo.", "error")
            return redirect(url_for("emprestimo.adicionar"))

    return render_template( "emprestimos/adicionar.html", usuarios=usuarios, itens=itens, hoje=hoje)

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
    emprestimo = Emprestimo.get(id)
    if not emprestimo:
        flash("Empréstimo não encontrado!", "error")
        return redirect(url_for("emprestimo.listar"))

    try:
        hoje = date.today()
        status = "devolvido"

        emprestimo.update(
            data_devolucao=hoje,
            status=status
        )

        # devolve item ao estoque
        item = Item.get(emprestimo.item_id)
        item.quantidade += 1
        item.save()

        flash("Devolução registrada com sucesso!", "success")
        return redirect(url_for("emprestimo.listar"))

    except Exception:
        db.session.rollback()
        flash("Erro ao registrar devolução.", "error")
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