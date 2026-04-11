from pydantic import BaseModel, Field
from flask_openapi3 import OpenAPI, Info, Tag
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Configurar informações da API
info = Info(title="ManutençãoAuto API", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Configurar banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Tag para organizar endpoints
greeting_tag = Tag(name="greeting", description="Endpoints de saudação")


# Modelo de resposta
class GreetingResponse(BaseModel):
    message: str = Field(..., description="Mensagem de saudação")


@app.get(
    "/",
    tags=[greeting_tag],
    summary="Saudação",
    description="Retorna uma mensagem de saudação simples",
    responses={"200": GreetingResponse}
)
def hello_world() -> dict:
    """Endpoint de saudação
    
    Retorna uma mensagem 'Hello, World!' em formato JSON.
    """
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    app.run(debug=True)