from flask_openapi3.models.info import Info
from flask_openapi3.openapi import OpenAPI
from flask_cors import CORS
from flask import redirect

from config import get_config_class
from manutencaoauto_api.db import init_db
from manutencaoauto_api.routes import register_routes


def create_app(config_class=None):
    info = Info(title="ManutençãoAuto API", version="1.0.0")
    app = OpenAPI(__name__, info=info)

    # Allow local frontend access (including file://, which sends Origin: null).
    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "null",
                    r"http://localhost(:\\d+)?",
                    r"http://127\\.0\\.0\\.1(:\\d+)?",
                ]
            }
        },
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type"],
    )

    # Configurar banco de dados
    if config_class is None:
        config_class = get_config_class()
    app.config.from_object(config_class)
    init_db(app)
    register_routes(app)

    @app.route("/")
    def redirect_to_swagger():
        return redirect("/openapi/swagger")

    return app


app = create_app()
