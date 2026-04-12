from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError

from manutencaoauto_api.db import db
from manutencaoauto_api.models import Manutencao_Servico, Servico
from manutencaoauto_api.schemas.common import ErrorResponse, IdPathParam, MessageResponse
from manutencaoauto_api.schemas.servico import (
    ServicoCriacao,
    ServicoListResponse,
    ServicoResponse,
)


servico_tag = Tag(name="servico", description="Endpoints de serviços")
servico_bp = APIBlueprint("servico", __name__)


@servico_bp.get(
    "/servicos",
    tags=[servico_tag],
    summary="Listar serviços",
    description="Retorna a lista de todos os serviços",
    responses={"200": ServicoListResponse}
)
def listar_servicos() -> list:
    servicos = Servico.query.all()
    servico_responses = [ServicoResponse(id=s.id, nome=s.nome, frequencia=s.frequencia, preco=s.preco) for s in servicos]
    return ServicoListResponse(servicos=servico_responses).model_dump()


@servico_bp.get(
    "/servicos/<int:id>",
    tags=[servico_tag],
    summary="Obter serviço por ID",
    description="Retorna um serviço específico pelo seu ID",
    responses={"200": ServicoResponse, "404": ErrorResponse}
)
def obter_servico(path: IdPathParam) -> dict:
    servico = Servico.query.get(path.id)
    if not servico:
        return ErrorResponse(error="Serviço não encontrado").model_dump(), 404
    return ServicoResponse(id=servico.id, nome=servico.nome, frequencia=servico.frequencia, preco=servico.preco).model_dump()


@servico_bp.post(
    "/servicos",
    tags=[servico_tag],
    summary="Criar serviço",
    description="Cria um novo serviço no banco de dados usando um payload JSON com nome, frequência e preço.",
    responses={"201": ServicoResponse, "400": ErrorResponse, "422": ErrorResponse}
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
        return ServicoResponse(id=novo_servico.id, nome=novo_servico.nome, frequencia=novo_servico.frequencia, preco=novo_servico.preco).model_dump(), 201
    except IntegrityError:
        db.session.rollback()
        return ErrorResponse(error="Serviço com este nome já existe ou erro de integridade").model_dump(), 400


@servico_bp.delete(
    "/servicos/<int:id>",
    tags=[servico_tag],
    summary="Deletar serviço",
    description="Deleta um serviço pelo seu ID. Retorna 409 se o serviço possui referências em manutenções",
    responses={"200": MessageResponse, "404": ErrorResponse, "409": ErrorResponse}
)
def deletar_servico(path: IdPathParam) -> dict:
    """Deleta um serviço

    Remove um serviço do banco de dados. Não permite deleção se há manutenções associadas.
    """
    servico = Servico.query.get(path.id)
    if not servico:
        return ErrorResponse(error="Serviço não encontrado").model_dump(), 404

    manutencao_servico = Manutencao_Servico.query.filter_by(id_servico=path.id).first()
    if manutencao_servico:
        return ErrorResponse(error="Serviço possui manutenções associadas e não pode ser deletado").model_dump(), 409

    try:
        db.session.delete(servico)
        db.session.commit()
        return MessageResponse(message="Serviço deletado com sucesso").model_dump(), 200
    except Exception as e:
        db.session.rollback()
        return ErrorResponse(error=f"Erro ao deletar serviço: {str(e)}").model_dump(), 400
