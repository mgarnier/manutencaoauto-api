from manutencaoauto_api.db.extensions import db


class Manutencao(db.Model):
    __tablename__ = "manutencao"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False)
    quilometragem = db.Column(db.Integer, nullable=False)
    data_prevista = db.Column(db.Date, nullable=True)
    data_realizada = db.Column(db.Date, nullable=True)

    __table_args__ = (
        db.CheckConstraint(
            "data_prevista IS NOT NULL OR data_realizada IS NOT NULL",
            name="ck_manutencao_data_informada",
        ),
    )

    def __repr__(self):
        return f"<Manutencao {self.descricao}>"
