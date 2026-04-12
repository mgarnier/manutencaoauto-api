import unittest

from app import create_app
from config import TestingConfig
from manutencaoauto_api.db import db


class ManutencaoServicoApiTestCase(unittest.TestCase):
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

    def _criar_manutencao(self) -> int:
        payload = {
            "descricao": "Revisão dos 50 mil",
            "quilometragem": 50000,
            "data_prevista": "2026-07-01",
            "data_realizada": None,
        }
        response = self.client.post("/manutencoes", json=payload)
        self.assertEqual(response.status_code, 201)
        return response.get_json()["id"]

    def _criar_servico(self) -> int:
        payload = {
            "nome": "Troca de óleo",
            "frequencia_km": 10000,
            "preco": 199.90,
        }
        response = self.client.post("/servicos", json=payload)
        self.assertEqual(response.status_code, 201)
        return response.get_json()["id"]

    def test_criar_associacao_valida_retorna_201(self):
        id_manutencao = self._criar_manutencao()
        id_servico = self._criar_servico()

        response = self.client.post(
            f"/manutencao-servicos?id_manutencao={id_manutencao}&id_servico={id_servico}",
            json={"preco": 149.90},
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["id_manutencao"], id_manutencao)
        self.assertEqual(data["id_servico"], id_servico)
        self.assertEqual(data["servico"]["id"], id_servico)
        self.assertEqual(data["manutencao"]["id"], id_manutencao)

    def test_criar_associacao_duplicada_retorna_409(self):
        id_manutencao = self._criar_manutencao()
        id_servico = self._criar_servico()
        path = f"/manutencao-servicos?id_manutencao={id_manutencao}&id_servico={id_servico}"

        first = self.client.post(path, json={"preco": 149.90})
        self.assertEqual(first.status_code, 201)

        second = self.client.post(path, json={"preco": 149.90})
        self.assertEqual(second.status_code, 409)

    def test_obter_associacao_inexistente_retorna_404(self):
        response = self.client.get("/manutencao-servicos/item?id_manutencao=999&id_servico=999")

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data.get("error"), "Associação manutenção-serviço não encontrada")

    def test_deletar_associacao_valida_retorna_200(self):
        id_manutencao = self._criar_manutencao()
        id_servico = self._criar_servico()
        path = f"/manutencao-servicos?id_manutencao={id_manutencao}&id_servico={id_servico}"

        create_response = self.client.post(path, json={"preco": 149.90})
        self.assertEqual(create_response.status_code, 201)

        delete_response = self.client.delete(path)
        self.assertEqual(delete_response.status_code, 200)

        get_response = self.client.get(
            f"/manutencao-servicos/item?id_manutencao={id_manutencao}&id_servico={id_servico}"
        )
        self.assertEqual(get_response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
