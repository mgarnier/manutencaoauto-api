import unittest
from decimal import Decimal

from app import create_app
from config import TestingConfig
from manutencaoauto_api.db import db


class ServicoApiTestCase(unittest.TestCase):
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

    def test_criar_servico(self):
        payload = {
            "nome": "Troca de óleo",
            "frequencia_km": 10000,
            "preco": 199.90,
        }
        response = self.client.post("/servicos", json=payload)
        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn("id", data)
        self.assertEqual(data["nome"], payload["nome"])
        self.assertEqual(data["frequencia_km"], payload["frequencia_km"])
        self.assertEqual(Decimal(str(data["preco"])), Decimal(str(payload["preco"])))

    def test_criar_servico_duplicado_retorna_400(self):
        payload = {
            "nome": "Alinhamento",
            "frequencia_km": 10000,
            "preco": 120.00,
        }
        first_response = self.client.post("/servicos", json=payload)
        self.assertEqual(first_response.status_code, 201)

        second_response = self.client.post("/servicos", json=payload)
        self.assertEqual(second_response.status_code, 400)
        data = second_response.get_json()
        self.assertEqual(data.get("error"), "Serviço com este nome já existe ou erro de integridade")


if __name__ == "__main__":
    unittest.main()
