from flask import Flask, render_template
from storage import init_app, db
import secrets
from flask_login import LoginManager
from models.users import User
from controllers.emprestimo_controller import emprestimo_bp
from controllers.itens_controller import item_bp
from controllers.users_controller import user_bp
from controllers.auth.auth_controller import auth_bp

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# inicializa db e cria tabelas
init_app(app)

@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403

app.register_blueprint(emprestimo_bp)
app.register_blueprint(item_bp)
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)