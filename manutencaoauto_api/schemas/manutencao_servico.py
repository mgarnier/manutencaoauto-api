from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ManutencaoServicoFiltroQuery(BaseModel):
    model_config = ConfigDict(title="ManutencaoServico Query Parameters")

    id_manutencao: int | None = Field(default=None, description="ID da manutenção")
    id_servico: int | None = Field(default=None, description="ID do serviço")


class ManutencaoServicoChaveQuery(BaseModel):
    model_config = ConfigDict(title="ManutencaoServico Composite Key")

    id_manutencao: int = Field(..., description="ID da manutenção")
    id_servico: int = Field(..., description="ID do serviço")


class ManutencaoServicoCriacao(BaseModel):
    model_config = ConfigDict(
        title="ManutencaoServico Request Body",
        json_schema_extra={
            "example": {
                "preco": 350.00,
            }
        },
    )

    preco: Decimal = Field(
        ...,
        description="Preço do serviço aplicado a esta manutenção",
    )


class ManutencaoServicoResumoServico(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID do serviço")
    nome: str = Field(..., description="Nome do serviço")


class ManutencaoServicoResumoManutencao(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID da manutenção")
    descricao: str = Field(..., description="Descrição da manutenção")


class ManutencaoServicoResponse(BaseModel):
    id_manutencao: int = Field(..., description="ID da manutenção")
    id_servico: int = Field(..., description="ID do serviço")
    preco: Decimal = Field(..., description="Preço associado")
    manutencao: ManutencaoServicoResumoManutencao = Field(
        ...,
        description="Resumo da manutenção",
    )
    servico: ManutencaoServicoResumoServico = Field(
        ...,
        description="Resumo do serviço",
    )


class ManutencaoServicoListResponse(BaseModel):
    manutencao_servicos: list[ManutencaoServicoResponse] = Field(
        ...,
        description="Lista de associações manutenção-serviço",
    )
