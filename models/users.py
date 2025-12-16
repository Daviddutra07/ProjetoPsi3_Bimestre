# models/users.py
from models import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "tb_usuarios"
    id = db.Column("usr_id", db.Integer, primary_key=True)
    email = db.Column("usr_email", db.String(150), unique=True, nullable=False)
    senha_hash = db.Column("usr_senha", db.String(200), nullable=False)
    nome = db.Column("usr_nome", db.String(150))
    cpf = db.Column("usr_cpf", db.String(14))
    perfil = db.Column("usr_perfil", db.String(20), default="usuario")

    def is_admin(self):
        return self.perfil == "admin"

    @classmethod
    def get(cls, user_id):
        return cls.query.get(user_id)
    
    @classmethod
    def all(cls):
        return cls.query.all()
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        return self

    def update(self, email=None, senha=None, nome=None, cpf=None):
        if email:
            self.email = email
        if senha:
            self.senha_hash = generate_password_hash(senha)
        if nome:
            self.nome = nome
        if cpf:
            self.cpf = cpf
        db.session.commit()
        return self
    
    @classmethod
    def delete(cls, user_id):
        usuario = cls.query.get(user_id)
        if not usuario:
            return False

        db.session.delete(usuario)
        db.session.commit()
        return True
