from typing import Any, cast

from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from sqlalchemy.orm import Session

from manutencaoauto_api.db import db
from manutencaoauto_api.exceptions import (
    ManutencaoComReferencias,
    ManutencaoDadosInvalidos,
    ManutencaoErroOperacao,
    ManutencaoNaoEncontrada,
)
from manutencaoauto_api.schemas.common import ErrorResponse, IdPathParam, MessageResponse
from manutencaoauto_api.schemas.manutencao import (
    ManutencaoCriacao,
    ManutencaoListResponse,
    ManutencaoResponse,
)
from manutencaoauto_api.services import ManutencaoService


manutencao_tag = Tag(name="manutencao", description="Endpoints de manutenções")
manutencao_bp = APIBlueprint("manutencao", __name__)
manutencao_service = ManutencaoService(cast(Session, db.session))

JsonDict = dict[str, Any]
RouteResponse = JsonDict | tuple[JsonDict, int]


@manutencao_bp.get(
    "/manutencoes",
    tags=[manutencao_tag],
    summary="Listar manutenções",
    description="Retorna a lista de todas as manutenções",
    responses={"200": ManutencaoListResponse},
)
def listar_manutencoes() -> JsonDict:
    manutencoes = manutencao_service.listar()
    manutencao_responses = [ManutencaoResponse.model_validate(m) for m in manutencoes]
    return ManutencaoListResponse(manutencoes=manutencao_responses).model_dump()


@manutencao_bp.get(
    "/manutencoes/<int:id>",
    tags=[manutencao_tag],
    summary="Obter manutenção por ID",
    description="Retorna uma manutenção específica pelo seu ID",
    responses={"200": ManutencaoResponse, "404": ErrorResponse},
)
def obter_manutencao(path: IdPathParam) -> RouteResponse:
    try:
        manutencao = manutencao_service.obter(path.id)
        return ManutencaoResponse.model_validate(manutencao).model_dump()
    except ManutencaoNaoEncontrada as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 404


@manutencao_bp.post(
    "/manutencoes",
    tags=[manutencao_tag],
    summary="Criar manutenção",
    description=(
        "Cria uma nova manutenção no banco de dados com descrição, quilometragem "
        "e ao menos uma data (prevista ou realizada)."
    ),
    responses={"201": ManutencaoResponse, "400": ErrorResponse, "422": ErrorResponse},
)
def criar_manutencao(body: ManutencaoCriacao) -> RouteResponse:
    try:
        manutencao = manutencao_service.criar(
            body.descricao,
            body.quilometragem,
            body.data_prevista,
            body.data_realizada,
        )
        return ManutencaoResponse.model_validate(manutencao).model_dump(), 201
    except ManutencaoDadosInvalidos as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 400
    except ManutencaoErroOperacao as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 400


@manutencao_bp.delete(
    "/manutencoes/<int:id>",
    tags=[manutencao_tag],
    summary="Deletar manutenção",
    description=(
        "Deleta uma manutenção pelo ID. Retorna 409 se a manutenção possuir "
        "serviços associados."
    ),
    responses={"200": MessageResponse, "404": ErrorResponse, "409": ErrorResponse},
)
def deletar_manutencao(path: IdPathParam) -> RouteResponse:
    try:
        manutencao_service.deletar(path.id)
        return MessageResponse(message="Manutenção deletada com sucesso").model_dump(), 200
    except ManutencaoNaoEncontrada as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 404
    except ManutencaoComReferencias as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 409
    except ManutencaoErroOperacao as exc:
        return ErrorResponse(error=str(exc)).model_dump(), 400
