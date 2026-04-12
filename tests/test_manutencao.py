import unittest

from app import create_app
from config import TestingConfig
from manutencaoauto_api.db import db


class ManutencaoApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_criar_manutencao_valida_retorna_201(self):
        payload = {
            "descricao": "Troca de correia",
            "quilometragem": 68000,
            "data_prevista": "2026-06-10",
            "data_realizada": None,
        }
        response = self.client.post("/manutencoes", json=payload)

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["descricao"], payload["descricao"])
        self.assertEqual(data["quilometragem"], payload["quilometragem"])

    def test_criar_manutencao_sem_datas_retorna_400(self):
        payload = {
            "descricao": "Revisão sem data",
            "quilometragem": 50000,
            "data_prevista": None,
            "data_realizada": None,
        }
        response = self.client.post("/manutencoes", json=payload)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data.get("error"), "Informe data_prevista ou data_realizada")

    def test_obter_manutencao_inexistente_retorna_404(self):
        response = self.client.get("/manutencoes/999")

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data.get("error"), "Manutenção não encontrada")


if __name__ == "__main__":
    unittest.main()
