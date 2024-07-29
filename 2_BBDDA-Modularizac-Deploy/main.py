from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router


# Creamos Una instancia de FastAPI
app = FastAPI()

# Para cambiar el nombre de la aplicacion
app.title = "Mi aplicación con FastAPI"

# Para cambiar la version de la aplicacion
app.version = "0.0.1"

# Agrega el middleware personalizado a la aplicación FastAPI.
# Esto permite que el ErrorHandler maneje errores en todas las solicitudes.
app.add_middleware(ErrorHandler)

# ROUTERS-------------------------------------------------
app.include_router(movie_router)
app.include_router(user_router)
# --------------------------------------------------------


# Base de Datos
Base.metadata.create_all(bind=engine)        


# Lista de varios diccionarios
movies = [ 
            {
                'id': 1,
                'title': 'Avatar',
                'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
                'year': '2009',
                'rating': 7.8,
                'category': 'Acción'    
            },
            {
                "id": 2,
                "title": "Avatar 2",
                "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
                "year": "2011",
                "rating": 5.8,
                "category": "Acción"
            }
        ]

# Indicamos la Ruta de inicio
@movie_router.get("/", tags=['Home']) # Los tags nos permiten agrupar las rutas
def función_root():
    return  HTMLResponse('<h2>Hola mundo usando HTML</h2>')


    







