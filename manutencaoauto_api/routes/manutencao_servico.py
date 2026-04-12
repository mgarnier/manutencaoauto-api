from typing import Any, cast

from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from sqlalchemy.orm import Session

from manutencaoauto_api.db import db
from manutencaoauto_api.exceptions import (
    ManutencaoErroOperacao,
    ManutencaoNaoEncontrada,
    ManutencaoServicoErroOperacao,
    ManutencaoServicoJaAssociado,
    ManutencaoServicoNaoEncontrado,
    ServicoNaoEncontrado,
)
from manutencaoauto_api.models import Manutencao, Servico
from manutencaoauto_api.schemas.common import ErrorResponse, MessageResponse
from manutencaoauto_api.schemas.manutencao_servico import (
    ManutencaoServicoChaveQuery,
    ManutencaoServicoCriacao,
    ManutencaoServicoFiltroQuery,
    ManutencaoServicoListResponse,
    ManutencaoServicoResponse,
    ManutencaoServicoResumoManutencao,
    ManutencaoServicoResumoServico,
)
from manutencaoauto_api.services import ManutencaoServicoService


manutencao_servico_tag = Tag(
    name="manutencao_servico",
    description="Endpoints de associação entre manutenções e serviços",
)
manutencao_servico_bp = APIBlueprint("manutencao_servico", __name__)
manutencao_servico_service = ManutencaoServicoService(cast(Session, db.session))

JsonDict = dict[str, Any]
RouteResponse = JsonDict | tuple[JsonDict, int]


def _to_response(item) -> ManutencaoServicoResponse:
    manutencao = cast(Manutencao, db.session.get(Manutencao, item.id_manutencao))
    servico = cast(Servico, db.session.get(Servico, item.id_servico))
    return ManutencaoServicoResponse(
        id_manutencao=item.id_manutencao,
        id_servico=item.id_servico,
        preco=item.preco,
        manutencao=ManutencaoServicoResumoManutencao.model_validate(manutencao),
        servico=ManutencaoServicoResumoServico.model_validate(servico),
    )


@manutencao_servico_bp.get(
    "/manutencao-servicos",
    tags=[manutencao_servico_tag],
    summary="Listar associações manutenção-serviço",
    description="Lista associações podendo filtrar por id_manutencao e id_servico",
    responses={"200": ManutencaoServicoListResponse},
)
def listar_manutencao_servicos(query: ManutencaoServicoFiltroQuery) -> JsonDict:
    itens = manutencao_servico_service.listar(query.id_manutencao, query.id_servico)
    response_items = [_to_response(item) for item in itens]
    return ManutencaoServicoListResponse(
        manutencao_servicos=response_items
    ).model_dump()


@manutencao_servico_bp.get(
    "/manutencao-servicos/item",
    tags=[manutencao_servico_tag],
    summary="Obter associação específica",
    description="Obtém uma associação específica por chave composta",
    responses={"200": ManutencaoServicoResponse, "404": ErrorResponse},
)
def obter_manutencao_servico(query: ManutencaoServicoChaveQuery) -> RouteResponse:
    try:
        item = manutencao_servico_service.obter(query.id_manutencao, query.id_servico)
        return _to_response(item).model_dump()
    except ManutencaoServicoNaoEncontrado as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 404


@manutencao_servico_bp.post(
    "/manutencao-servicos",
    tags=[manutencao_servico_tag],
    summary="Criar associação manutenção-serviço",
    description="Cria uma associação entre manutenção e serviço com preço associado",
    responses={"201": ManutencaoServicoResponse, "400": ErrorResponse, "404": ErrorResponse, "409": ErrorResponse, "422": ErrorResponse},
)
def criar_manutencao_servico(
    query: ManutencaoServicoChaveQuery,
    body: ManutencaoServicoCriacao,
) -> RouteResponse:
    try:
        item = manutencao_servico_service.criar(
            query.id_manutencao,
            query.id_servico,
            body.preco,
        )
        return _to_response(item).model_dump(), 201
    except ManutencaoServicoJaAssociado as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 409
    except ManutencaoNaoEncontrada as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 404
    except ServicoNaoEncontrado as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 404
    except (ManutencaoServicoErroOperacao, ManutencaoErroOperacao) as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 400


@manutencao_servico_bp.delete(
    "/manutencao-servicos",
    tags=[manutencao_servico_tag],
    summary="Deletar associação manutenção-serviço",
    description="Remove uma associação entre manutenção e serviço",
    responses={"200": MessageResponse, "404": ErrorResponse, "400": ErrorResponse},
)
def deletar_manutencao_servico(query: ManutencaoServicoChaveQuery) -> RouteResponse:
    try:
        manutencao_servico_service.deletar(query.id_manutencao, query.id_servico)
        return MessageResponse(
            message="Associação manutenção-serviço deletada com sucesso"
        ).model_dump(), 200
    except ManutencaoServicoNaoEncontrado as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 404
    except ManutencaoServicoErroOperacao as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 400
