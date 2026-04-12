from flask_openapi3 import OpenAPI, Info

from config import get_config_class
from manutencaoauto_api.db import init_db
from manutencaoauto_api.routes.servico import servico_bp


info = Info(title="ManutençãoAuto API", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Configurar banco de dados
app.config.from_object(get_config_class())
init_db(app)
app.register_api(servico_bp)
