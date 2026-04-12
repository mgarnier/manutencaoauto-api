from typing import Any, cast

from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from sqlalchemy.orm import Session

from manutencaoauto_api.db import db
from manutencaoauto_api.exceptions import (
    ServicoComReferencias,
    ServicoErroOperacao,
    ServicoJaExiste,
    ServicoNaoEncontrado,
)
from manutencaoauto_api.schemas.common import ErrorResponse, IdPathParam, MessageResponse
from manutencaoauto_api.schemas.servico import (
    ServicoCriacao,
    ServicoListResponse,
    ServicoResponse,
)
from manutencaoauto_api.services import ServicoService


servico_tag = Tag(name="servico", description="Endpoints de serviços")
servico_bp = APIBlueprint("servico", __name__)
servico_service = ServicoService(cast(Session, db.session))

JsonDict = dict[str, Any]
RouteResponse = JsonDict | tuple[JsonDict, int]


@servico_bp.get(
    "/servicos",
    tags=[servico_tag],
    summary="Listar serviços",
    description="Retorna a lista de todos os serviços",
    responses={"200": ServicoListResponse}
)
def listar_servicos() -> JsonDict:
    servicos = servico_service.listar()
    servico_responses = [ServicoResponse.model_validate(s) for s in servicos]
    return ServicoListResponse(servicos=servico_responses).model_dump()


@servico_bp.get(
    "/servicos/<int:id>",
    tags=[servico_tag],
    summary="Obter serviço por ID",
    description="Retorna um serviço específico pelo seu ID",
    responses={"200": ServicoResponse, "404": ErrorResponse}
)
def obter_servico(path: IdPathParam) -> RouteResponse:
    try:
        servico = servico_service.obter(path.id)
        return ServicoResponse.model_validate(servico).model_dump()
    except ServicoNaoEncontrado as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 404


@servico_bp.post(
    "/servicos",
    tags=[servico_tag],
    summary="Criar serviço",
    description=(
        "Cria um novo serviço no banco de dados usando um payload JSON "
        "com nome, frequência e preço."
    ),
    responses={"201": ServicoResponse, "400": ErrorResponse, "422": ErrorResponse}
)
def criar_servico(body: ServicoCriacao) -> RouteResponse:
    """Cria um novo serviço usando o corpo JSON.

    Recebe os dados do serviço e o salva no banco de dados.
    O body é validado pelo schema ServicoCriacao.
    """
    try:
        novo_servico = servico_service.criar(body.nome, body.frequencia, body.preco)
        return ServicoResponse.model_validate(novo_servico).model_dump(), 201
    except ServicoJaExiste as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 400


@servico_bp.delete(
    "/servicos/<int:id>",
    tags=[servico_tag],
    summary="Deletar serviço",
    description=(
        "Deleta um serviço pelo seu ID. Retorna 409 se o serviço "
        "possui referências em manutenções"
    ),
    responses={"200": MessageResponse, "404": ErrorResponse, "409": ErrorResponse}
)
def deletar_servico(path: IdPathParam) -> RouteResponse:
    """Deleta um serviço

    Remove um serviço do banco de dados. Não permite deleção se há manutenções associadas.
    """
    try:
        servico_service.deletar(path.id)
        return MessageResponse(message="Serviço deletado com sucesso").model_dump(), 200
    except ServicoNaoEncontrado as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 404
    except ServicoComReferencias as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 409
    except ServicoErroOperacao as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 400
