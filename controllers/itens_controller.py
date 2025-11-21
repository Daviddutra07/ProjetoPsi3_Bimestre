from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from models.itens import Item

item_bp = Blueprint("item", __name__, url_prefix='/itens', template_folder='templates/itens')

@item_bp.route("/")
@login_required
def itens():
    itens = Item.all()
    return render_template("itens/itens.html", itens=itens)

@item_bp.route("/adicionar", methods = ["GET", "POST"])
@login_required
def adicionar():
    if request.method == "POST":
        item = Item(nome=request.form["nome"], categoria=(request.form["categoria"]), quantidade = int(request.form["quantidade"]))

        item.save()
        flash("Produto adicionado com sucesso!", "success")
        return redirect(url_for("item.itens"))
    
    return render_template("itens/adicionar.html")

@item_bp.route("/editar/<int:id>", methods = ["GET", "POST"])
@login_required
def editar(id):
    i = Item.get(id)
    if not i:
        flash("Item não encontrado!", "error")
        return redirect(url_for("item.itens"))

    if request.method == "POST":
        i.update(nome=request.form.get("nome"),categoria=(request.form.get("categoria")),quantidade=int(request.form.get("quantidade", 0)))
        flash("Item editado!", "success")
        return redirect(url_for("item.itens"))

    return render_template('itens/editar.html', item=i)

@item_bp.route('/deletar/<int:id>', methods = ["POST"])
@login_required
def remover(id):
    i = Item.get(id)

    if i:
        try:
            i.delete()
            flash("Item removido com sucesso!", "success")
        except:
            flash(f"Não foi possível remover este gênero.", "error")
    else:
        flash(f"Item não encontrado, tente novamente.", "error")
    return redirect(url_for("item.itens"))