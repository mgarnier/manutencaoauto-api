import unittest
from datetime import date
from decimal import Decimal

from app import create_app
from config import TestingConfig
from manutencaoauto_api.db import db
from manutencaoauto_api.exceptions import (
    ServicoComReferencias,
    ServicoJaExiste,
    ServicoNaoEncontrado,
)
from manutencaoauto_api.models import Manutencao, ManutencaoServico
from manutencaoauto_api.services import ServicoService


class ServicoServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.service = ServicoService(db.session)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_criar_servico_com_sucesso(self):
        servico = self.service.criar("Troca de óleo", 10000, Decimal("199.90"))

        self.assertIsNotNone(servico.id)
        self.assertEqual(servico.nome, "Troca de óleo")
        self.assertEqual(servico.frequencia_km, 10000)
        self.assertEqual(servico.preco, Decimal("199.90"))

    def test_criar_servico_duplicado_lanca_erro(self):
        self.service.criar("Alinhamento", 10000, Decimal("120.00"))

        with self.assertRaises(ServicoJaExiste):
            self.service.criar("Alinhamento", 10000, Decimal("120.00"))

    def test_obter_servico_inexistente_lanca_erro(self):
        with self.assertRaises(ServicoNaoEncontrado):
            self.service.obter(999)

    def test_deletar_servico_com_referencias_lanca_erro(self):
        servico = self.service.criar("Revisão", 40000, Decimal("450.00"))
        manutencao = Manutencao(
            descricao="Revisão anual",
            quilometragem=45000,
            data_prevista=date.today(),
            data_realizada=None,
        )
        db.session.add(manutencao)
        db.session.commit()

        associacao = ManutencaoServico(
            id_manutencao=manutencao.id,
            id_servico=servico.id,
            preco=Decimal("450.00"),
        )
        db.session.add(associacao)
        db.session.commit()

        with self.assertRaises(ServicoComReferencias):
            self.service.deletar(servico.id)


if __name__ == "__main__":
    unittest.main()
