from manutencaoauto_api.db.extensions import db


class ManutencaoServico(db.Model):
    __tablename__ = "manutencao_servico"

    id_manutencao = db.Column(
        db.Integer,
        db.ForeignKey("manutencao.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    id_servico = db.Column(
        db.Integer,
        db.ForeignKey("servico.id"),
        primary_key=True,
        nullable=False,
    )
    preco = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<ManutencaoServico manutencao={self.id_manutencao} servico={self.id_servico}>"
