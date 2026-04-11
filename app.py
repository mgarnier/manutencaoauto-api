from pydantic import BaseModel, Field
from flask_openapi3 import OpenAPI, Info, Tag
from flask_sqlalchemy import SQLAlchemy
from config import Config
from database import db
from models import Servico
from sqlalchemy.exc import IntegrityError
info = Info(title="ManutençãoAuto API", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Configurar banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Tag para organizar endpoints
greeting_tag = Tag(name="greeting", description="Endpoints de saudação")
servico_tag = Tag(name="servico", description="Endpoints de serviços")


# Modelo de resposta
class GreetingResponse(BaseModel):
    message: str = Field(..., description="Mensagem de saudação")


class ServicoCriacao(BaseModel):
    nome: str = Field(..., description="Nome do serviço")
    frequencia: int = Field(..., description="Frequência do serviço em dias")
    preco: float = Field(..., description="Preço do serviço")


class ServicoResponse(BaseModel):
    id: int = Field(..., description="ID do serviço")
    nome: str = Field(..., description="Nome do serviço")
    frequencia: int = Field(..., description="Frequência do serviço em dias")
    preco: float = Field(..., description="Preço do serviço")


@app.get(
    "/",
    tags=[greeting_tag],
    summary="Saudação",
    description="Retorna uma mensagem de saudação simples",
    responses={"200": GreetingResponse}
)
def hello_world() -> dict:
    """Endpoint de saudação
    
    Retorna uma mensagem 'Hello, World!' em formato JSON.
    """
    return {"message": "Hello, World!"}


@app.post(
    "/servicos",
    tags=[servico_tag],
    summary="Criar serviço",
    description="Cria um novo serviço no banco de dados",
    responses={"201": ServicoResponse, "400": {"description": "Erro de validação ou integridade"}}
)
def criar_servico(body: ServicoCriacao) -> dict:
    """Cria um novo serviço
    
    Recebe os dados do serviço e o salva no banco de dados.
    """
    try:
        novo_servico = Servico(nome=body.nome, frequencia=body.frequencia, preco=body.preco)
        db.session.add(novo_servico)
        db.session.commit()
        return ServicoResponse(id=novo_servico.id, nome=novo_servico.nome, frequencia=novo_servico.frequencia, preco=novo_servico.preco).dict(), 201
    except IntegrityError:
        db.session.rollback()
        return {"error": "Serviço com este nome já existe ou erro de integridade"}, 400