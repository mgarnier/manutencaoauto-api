from pydantic import BaseModel, Field
from flask_openapi3 import OpenAPI, Info, Tag
from flask_sqlalchemy import SQLAlchemy
from config import Config
from database import db
from models import Servico, Manutencao_Servico
from sqlalchemy.exc import IntegrityError
from flask import abort
from typing import List
info = Info(title="ManutençãoAuto API", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Configurar banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Tag para organizar endpoints
servico_tag = Tag(name="servico", description="Endpoints de serviços")


class ServicoCriacao(BaseModel):
    class Config:
        title = "Servico Request Body"
        schema_extra = {
            "example": {
                "nome": "Troca de óleo",
                "frequencia": 90,
                "preco": 199.90
            }
        }

    nome: str = Field(..., description="Nome do serviço")
    frequencia: int = Field(..., description="Frequência do serviço em dias")
    preco: float = Field(..., description="Preço do serviço")


class ServicoResponse(BaseModel):
    id: int = Field(..., description="ID do serviço")
    nome: str = Field(..., description="Nome do serviço")
    frequencia: int = Field(..., description="Frequência do serviço em dias")
    preco: float = Field(..., description="Preço do serviço")


class ServicoListResponse(BaseModel):
    servicos: List[ServicoResponse] = Field(..., description="Lista de serviços")


class ServicoPathParam(BaseModel):
    class Config:
        title = "Servico Path Parameters"
    
    id: int = Field(..., description="ID do serviço")


class ServicoDeletadoResponse(BaseModel):
    message: str = Field(..., description="Mensagem de confirmação")


class ServicoErroResponse(BaseModel):
    class Config:
        title = "Servico Error Response"

    error: str = Field(..., description="Mensagem de erro ao processar a requisição")


@app.post(
    "/servicos",
    tags=[servico_tag],
    summary="Criar serviço",
    description="Cria um novo serviço no banco de dados usando um payload JSON com nome, frequência e preço.",
    responses={"201": ServicoResponse, "400": ServicoErroResponse, "422": {"description": "Body inválido ou dados de validação incorretos"}}
)
def criar_servico(body: ServicoCriacao) -> dict:
    """Cria um novo serviço usando o corpo JSON.
    
    Recebe os dados do serviço e o salva no banco de dados.
    O body é validado pelo schema ServicoCriacao.
    """
    try:
        novo_servico = Servico(nome=body.nome, frequencia=body.frequencia, preco=body.preco)
        db.session.add(novo_servico)
        db.session.commit()
        return ServicoResponse(id=novo_servico.id, nome=novo_servico.nome, frequencia=novo_servico.frequencia, preco=novo_servico.preco).dict(), 201
    except IntegrityError:
        db.session.rollback()
        return {"error": "Serviço com este nome já existe ou erro de integridade"}, 400


@app.get(
    "/servicos",
    tags=[servico_tag],
    summary="Listar serviços",
    description="Retorna a lista de todos os serviços",
    responses={"200": ServicoListResponse}
)
def listar_servicos() -> list:
    servicos = Servico.query.all()
    servico_responses = [ServicoResponse(id=s.id, nome=s.nome, frequencia=s.frequencia, preco=s.preco) for s in servicos]
    return ServicoListResponse(servicos=servico_responses).dict()


@app.get(
    "/servicos/<int:id>",
    tags=[servico_tag],
    summary="Obter serviço por ID",
    description="Retorna um serviço específico pelo seu ID",
    responses={"200": ServicoResponse, "404": ServicoErroResponse}
)
def obter_servico(path: ServicoPathParam) -> dict:
    servico = Servico.query.get(path.id)
    if not servico:
        return ServicoErroResponse(error="Serviço não encontrado").dict(), 404
    return ServicoResponse(id=servico.id, nome=servico.nome, frequencia=servico.frequencia, preco=servico.preco).dict()


@app.delete(
    "/servicos/<int:id>",
    tags=[servico_tag],
    summary="Deletar serviço",
    description="Deleta um serviço pelo seu ID. Retorna 409 se o serviço possui referências em manutenções",
    responses={"200": ServicoDeletadoResponse, "404": ServicoErroResponse, "409": ServicoErroResponse}
)
def deletar_servico(path: ServicoPathParam) -> dict:
    """Deleta um serviço
    
    Remove um serviço do banco de dados. Não permite deleção se há manutenções associadas.
    """
    servico = Servico.query.get(path.id)
    if not servico:
        return ServicoErroResponse(error="Serviço não encontrado").dict(), 404
    
    # Verificar se existem registros relacionados em manutencao_servico
    manutencao_servico = Manutencao_Servico.query.filter_by(id_servico=path.id).first()
    if manutencao_servico:
        return ServicoErroResponse(error="Serviço possui manutenções associadas e não pode ser deletado").dict(), 409
    
    try:
        db.session.delete(servico)
        db.session.commit()
        return ServicoDeletadoResponse(message="Serviço deletado com sucesso").dict(), 200
    except Exception as e:
        db.session.rollback()
        return ServicoErroResponse(error=f"Erro ao deletar serviço: {str(e)}").dict(), 400