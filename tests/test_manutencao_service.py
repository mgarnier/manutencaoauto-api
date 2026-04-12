import unittest
from datetime import date

from app import create_app
from config import TestingConfig
from manutencaoauto_api.db import db
from manutencaoauto_api.exceptions import (
    ManutencaoComReferencias,
    ManutencaoDadosInvalidos,
    ManutencaoNaoEncontrada,
)
from manutencaoauto_api.models import ManutencaoServico, Servico
from manutencaoauto_api.services import ManutencaoService


class ManutencaoServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.service = ManutencaoService(db.session)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_criar_manutencao_com_sucesso(self):
        manutencao = self.service.criar(
            "Troca de correia",
            70000,
            date.today(),
            None,
        )

        self.assertIsNotNone(manutencao.id)
        self.assertEqual(manutencao.descricao, "Troca de correia")
        self.assertEqual(manutencao.quilometragem, 70000)

    def test_criar_sem_datas_lanca_erro(self):
        with self.assertRaises(ManutencaoDadosInvalidos):
            self.service.criar("Revisão", 50000, None, None)

    def test_obter_inexistente_lanca_erro(self):
        with self.assertRaises(ManutencaoNaoEncontrada):
            self.service.obter(999)

    def test_deletar_com_referencias_lanca_erro(self):
        manutencao = self.service.criar(
            "Revisão completa",
            52000,
            date.today(),
            None,
        )
        servico = Servico()
        servico.nome = "Alinhamento"
        servico.frequencia = 180
        servico.preco = 120
        db.session.add(servico)
        db.session.commit()

        associacao = ManutencaoServico()
        associacao.id_manutencao = manutencao.id
        associacao.id_servico = servico.id
        associacao.preco = 120
        db.session.add(associacao)
        db.session.commit()

        with self.assertRaises(ManutencaoComReferencias):
            self.service.deletar(manutencao.id)


if __name__ == "__main__":
    unittest.main()
