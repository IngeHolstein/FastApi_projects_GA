from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        # Inicializa el middleware con la aplicación FastAPI.
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        # Procesa la solicitud, capturando cualquier excepción para devolver un error 500.
        try:
            # Pasa la solicitud al siguiente middleware o ruta.
            return await call_next(request) # Se ejecutará la siguiente función si no hubo errores
        except Exception as e:
            # Captura cualquier excepción y devuelve una respuesta JSON con el error.
            return JSONResponse(status_code=500, content={'error': str(e)})
