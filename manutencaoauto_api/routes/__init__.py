from manutencaoauto_api.routes.manutencao import manutencao_bp
from manutencaoauto_api.routes.manutencao_servico import manutencao_servico_bp
from manutencaoauto_api.routes.servico import servico_bp


def register_routes(app) -> None:
    app.register_api(manutencao_bp)
    app.register_api(manutencao_servico_bp)
    app.register_api(servico_bp)
