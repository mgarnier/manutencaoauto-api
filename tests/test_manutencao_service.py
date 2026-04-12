import unittest
from datetime import date

from sqlalchemy import select

from app import create_app
from config import TestingConfig
from manutencaoauto_api.db import db
from manutencaoauto_api.exceptions import (
    ManutencaoDadosInvalidos,
    ManutencaoNaoEncontrada,
)
from manutencaoauto_api.models import Manutencao, ManutencaoServico, Servico
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

    def test_deletar_com_referencias_remove_associacoes(self):
        manutencao = self.service.criar(
            "Revisão completa",
            52000,
            date.today(),
            None,
        )
        servico = Servico()
        servico.nome = "Alinhamento"
        servico.frequencia_km = 10000
        servico.preco = 120
        db.session.add(servico)
        db.session.commit()

        associacao = ManutencaoServico()
        associacao.id_manutencao = manutencao.id
        associacao.id_servico = servico.id
        associacao.preco = 120
        db.session.add(associacao)
        db.session.commit()

        self.service.deletar(manutencao.id)

        manutencao_removida = db.session.get(Manutencao, manutencao.id)
        associacao_removida = db.session.execute(
            select(ManutencaoServico).filter_by(
                id_manutencao=manutencao.id,
                id_servico=servico.id,
            )
        ).scalar_one_or_none()

        self.assertIsNone(manutencao_removida)
        self.assertIsNone(associacao_removida)


if __name__ == "__main__":
    unittest.main()
