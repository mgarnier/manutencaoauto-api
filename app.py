from flask_openapi3.models.info import Info
from flask_openapi3.openapi import OpenAPI

from config import get_config_class
from manutencaoauto_api.db import init_db
from manutencaoauto_api.routes import register_routes


def create_app(config_class=None):
    info = Info(title="ManutençãoAuto API", version="1.0.0")
    app = OpenAPI(__name__, info=info)

    # Configurar banco de dados
    if config_class is None:
        config_class = get_config_class()
    app.config.from_object(config_class)
    init_db(app)
    register_routes(app)

    return app


app = create_app()
