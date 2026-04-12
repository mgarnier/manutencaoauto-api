from manutencaoauto_api.db.extensions import db


class Servico(db.Model):
    __tablename__ = "servico"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    frequencia_km = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<Servico {self.nome}>"
