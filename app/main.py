from api.router import router as api_router
from fastapi import FastAPI


app = FastAPI(title="Microserviço de Gerenciamento de Usuários",
              description="""Este é um microserviço para
              gerenciamento de usuários. Ele fornece endpoints para
              autenticação, cadastro,
              recuperação de senha e operações CRUD de usuários.""",
              version="1.0.0")

app.include_router(api_router)
