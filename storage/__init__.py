from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# Ativar foreign keys no SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()

def init_app(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

        from models.users import User

        admin = User.query.filter_by(email="admin@admin.com").first()
        if not admin:
            admin = User(
                email="admin@admin.com",
                nome="Administrador",
                senha_hash=generate_password_hash("admin"),
                perfil="admin"
            )
            db.session.add(admin)
            
            db.session.commit()
