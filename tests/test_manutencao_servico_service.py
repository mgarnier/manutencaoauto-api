import unittest
from datetime import date
from decimal import Decimal

from app import create_app
from config import TestingConfig
from manutencaoauto_api.db import db
from manutencaoauto_api.exceptions import (
    ManutencaoNaoEncontrada,
    ManutencaoServicoJaAssociado,
    ManutencaoServicoNaoEncontrado,
    ServicoNaoEncontrado,
)
from manutencaoauto_api.models import Manutencao, Servico
from manutencaoauto_api.services import ManutencaoServicoService


class ManutencaoServicoServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.service = ManutencaoServicoService(db.session)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _criar_manutencao(self) -> Manutencao:
        manutencao = Manutencao()
        manutencao.descricao = "Revisão"
        manutencao.quilometragem = 50000
        manutencao.data_prevista = date.today()
        manutencao.data_realizada = None
        db.session.add(manutencao)
        db.session.commit()
        return manutencao

    def _criar_servico(self) -> Servico:
        servico = Servico()
        servico.nome = "Alinhamento"
        servico.frequencia_km = 10000
        servico.preco = Decimal("120.00")
        db.session.add(servico)
        db.session.commit()
        return servico

    def test_criar_associacao_com_sucesso(self):
        manutencao = self._criar_manutencao()
        servico = self._criar_servico()

        assoc = self.service.criar(manutencao.id, servico.id, Decimal("99.90"))

        self.assertEqual(assoc.id_manutencao, manutencao.id)
        self.assertEqual(assoc.id_servico, servico.id)
        self.assertEqual(assoc.preco, Decimal("99.90"))

    def test_criar_associacao_duplicada_lanca_erro(self):
        manutencao = self._criar_manutencao()
        servico = self._criar_servico()
        self.service.criar(manutencao.id, servico.id, Decimal("99.90"))

        with self.assertRaises(ManutencaoServicoJaAssociado):
            self.service.criar(manutencao.id, servico.id, Decimal("99.90"))

    def test_criar_associacao_com_manutencao_inexistente_lanca_erro(self):
        servico = self._criar_servico()

        with self.assertRaises(ManutencaoNaoEncontrada):
            self.service.criar(999, servico.id, Decimal("99.90"))

    def test_criar_associacao_com_servico_inexistente_lanca_erro(self):
        manutencao = self._criar_manutencao()

        with self.assertRaises(ServicoNaoEncontrado):
            self.service.criar(manutencao.id, 999, Decimal("99.90"))

    def test_obter_inexistente_lanca_erro(self):
        with self.assertRaises(ManutencaoServicoNaoEncontrado):
            self.service.obter(1, 1)

    def test_deletar_associacao_com_sucesso(self):
        manutencao = self._criar_manutencao()
        servico = self._criar_servico()
        self.service.criar(manutencao.id, servico.id, Decimal("99.90"))

        self.service.deletar(manutencao.id, servico.id)

        with self.assertRaises(ManutencaoServicoNaoEncontrado):
            self.service.obter(manutencao.id, servico.id)


if __name__ == "__main__":
    unittest.main()
