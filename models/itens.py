from models import db

class Item(db.Model):
    __tablename__ = "tb_itens"
    id = db.Column("itm_id", db.Integer, primary_key=True)
    nome = db.Column("itm_nome", db.String(150))
    categoria = db.Column("itm_categoria", db.String(50), nullable = True)
    quantidade = db.Column("itm_quantidade", db.Integer, nullable=False)

    @classmethod
    def buscar(cls, termo=None):
        query = cls.query

        if termo:
            query = query.filter(
                cls.nome.ilike(f"%{termo}%")
            )

        return query.order_by(cls.nome).all()


    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def all(cls):
        return cls.query.all()

    def update(self, nome=None, categoria=None, quantidade=None):
        if nome:
            self.nome = nome
        if categoria:
            self.categoria = categoria
        if quantidade is not None:
            self.quantidade = quantidade

        db.session.commit()
        return self


    def delete(self):
        db.session.delete(self)
        db.session.commit()