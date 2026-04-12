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


class ServicoPathParam(BaseModel):
    model_config = ConfigDict(title="Servico Path Parameters")

    id: int = Field(..., description="ID do serviço")


class ServicoDeletadoResponse(BaseModel):
    message: str = Field(..., description="Mensagem de confirmação")


class ServicoErroResponse(BaseModel):
    model_config = ConfigDict(
        title="Servico Error Response",
        json_schema_extra={
            "example": {
                "error": "Serviço não encontrado"
            }
        },
    )

    error: str = Field(..., description="Mensagem de erro ao processar a requisição")