from database import db

class Servico(db.Model):
    __tablename__ = 'servico'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    frequencia = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<Serviço {self.nome}>'

class Manutencao(db.Model):
    __tablename__ = 'manutencao'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False)
    quilometragem = db.Column(db.Integer, nullable=False)
    data_prevista = db.Column(db.Date, nullable=True)
    data_realizada = db.Column(db.Date, nullable=True)

    __table_args__ = (
        db.CheckConstraint(
            'data_prevista IS NOT NULL OR data_realizada IS NOT NULL',
            name='ck_manutencao_data_informada'
        ),
    )

    def __repr__(self):
        return f'<Manutenção {self.descricao}>'

class Manutencao_Servico(db.Model):
    __tablename__ = 'manutencao_servico'
    id_manutencao = db.Column(db.Integer, db.ForeignKey('manutencao.id'), primary_key=True, nullable=False)
    id_servico = db.Column(db.Integer, db.ForeignKey('servico.id'), primary_key=True, nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<Manutencao_Servico manutencao={self.id_manutencao} servico={self.id_servico}>'