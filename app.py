from flask_openapi3 import OpenAPI, Info

from database import db
from manutencaoauto_api.routes.servico import servico_bp


info = Info(title="ManutençãoAuto API", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Configurar banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_api(servico_bp)

with app.app_context():
    db.create_all()
