# ManutencaoAuto API

API REST para gerenciamento de manutenções, serviços e relacionamento entre manutenções e serviços.

## Instalação

### Pre-requisitos
- Python 3.10 ou superior
- Pip
- Windows PowerShell ou Prompt de Comando

### Configuração do ambiente local
1. Acesse a pasta do projeto:
   cd manutencaoauto-api
2. Crie o ambiente virtual:
   .\createvenv.bat
3. Ative o ambiente virtual:
   .\activatevenv.bat
4. Instale as dependências:
   .\installreqs.bat

## Inicialização

### Executar a API
1. Na pasta manutencaoauto-api, execute:
   .\runflask.bat
2. A API será iniciada em http://localhost:5000.

## Testes

Para executar os testes automatizados:
1. Na pasta manutencaoauto-api, execute:
   .\runtests.bat

## Acesso rápido

- Swagger UI: http://localhost:5000/openapi/swagger
