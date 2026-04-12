from pydantic import BaseModel, ConfigDict, Field


class IdPathParam(BaseModel):
    model_config = ConfigDict(title="ID Path Parameters")

    id: int = Field(..., description="ID do recurso")


class MessageResponse(BaseModel):
    message: str = Field(..., description="Mensagem de confirmação")


class ErrorResponse(BaseModel):
    model_config = ConfigDict(
        title="Error Response",
        json_schema_extra={
            "example": {
                "error": "Recurso não encontrado"
            }
        },
    )

    error: str = Field(..., description="Mensagem de erro ao processar a requisição")