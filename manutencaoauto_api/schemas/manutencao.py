from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ManutencaoCriacao(BaseModel):
    model_config = ConfigDict(
        title="Manutencao Request Body",
        json_schema_extra={
            "example": {
                "descricao": "Troca de correia",
                "quilometragem": 65000,
                "data_prevista": "2026-05-10",
                "data_realizada": None,
            }
        },
    )

    descricao: str = Field(..., description="Descrição da manutenção")
    quilometragem: int = Field(..., description="Quilometragem da manutenção")
    data_prevista: date | None = Field(
        default=None,
        description="Data prevista da manutenção",
    )
    data_realizada: date | None = Field(
        default=None,
        description="Data em que a manutenção foi realizada",
    )


class ManutencaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID da manutenção")
    descricao: str = Field(..., description="Descrição da manutenção")
    quilometragem: int = Field(..., description="Quilometragem da manutenção")
    data_prevista: date | None = Field(
        default=None,
        description="Data prevista da manutenção",
    )
    data_realizada: date | None = Field(
        default=None,
        description="Data em que a manutenção foi realizada",
    )


class ManutencaoListResponse(BaseModel):
    manutencoes: list[ManutencaoResponse] = Field(
        ...,
        description="Lista de manutenções",
    )
