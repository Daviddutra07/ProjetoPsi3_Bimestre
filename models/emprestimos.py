from datetime import date, datetime
from models import db

class Emprestimo(db.Model):
    __tablename__ = "tb_emprestimos"

    id = db.Column("l_id", db.Integer, primary_key=True)
    user_id = db.Column("emp_usr_id", db.Integer, db.ForeignKey("tb_usuarios.usr_id"), nullable=False)
    item_id = db.Column("emp_itm_id", db.Integer, db.ForeignKey("tb_itens.itm_id"))
    data_emprestimo = db.Column( "emp_data_emprestimo", db.DateTime, default=datetime.now)
    data_devolucao = db.Column("emp_data_devolucao",db.DateTime,nullable=True)
    status = db.Column("emp_status", db.String(20),default="pendente")  # pendente, devolvido
    user = db.relationship("User", backref="emprestimos")
    item = db.relationship("Item", backref="emprestimos")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        return  self

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def all(cls):
        return cls.query.all()

    def update(self, user_id=None, item_id=None, data_emprestimo=None, data_devolucao=None, status=None):
        
        if user_id is not None:
            self.user_id = user_id
        
        if item_id is not None:
            self.item_id = item_id
        
        if data_emprestimo is not None:
            self.data_emprestimo = data_emprestimo
        
        if data_devolucao is not None:
            self.data_devolucao = data_devolucao
        
        if status is not None:
            self.status = status
        
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def ativos_por_usuario(cls, user_id):
        return cls.query.filter_by(user_id=user_id,status="pendente").count()