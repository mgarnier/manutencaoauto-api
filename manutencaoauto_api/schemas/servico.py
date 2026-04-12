from pydantic import BaseModel, ConfigDict, Field


class ServicoCriacao(BaseModel):
    model_config = ConfigDict(
        title="Servico Request Body",
        json_schema_extra={
            "example": {
                "nome": "Troca de óleo",
                "frequencia": 90,
                "preco": 199.90,
            }
        },
    )

    nome: str = Field(..., description="Nome do serviço")
    frequencia: int = Field(..., description="Frequência do serviço em dias")
    preco: float = Field(..., description="Preço do serviço")


class ServicoResponse(BaseModel):
    id: int = Field(..., description="ID do serviço")
    nome: str = Field(..., description="Nome do serviço")
    frequencia: int = Field(..., description="Frequência do serviço em dias")
    preco: float = Field(..., description="Preço do serviço")


class ServicoListResponse(BaseModel):
    servicos: list[ServicoResponse] = Field(..., description="Lista de serviços")
