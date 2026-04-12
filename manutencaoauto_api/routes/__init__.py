from manutencaoauto_api.routes.servico import servico_bp


def register_routes(app) -> None:
	app.register_api(servico_bp)
