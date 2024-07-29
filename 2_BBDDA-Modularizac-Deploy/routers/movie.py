from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie


movie_router = APIRouter()


# Consulta de datos, Lectura
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    db = Session()
    lectura = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(lectura))


# Consulta a la Base de datos por id
@movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    lectura = MovieService(db).get_movie(id)
    if lectura:
        return JSONResponse(status_code=200, content=jsonable_encoder(lectura))
    return JSONResponse(status_code=404, content={"message": "Película inexistente en la base de datos"})


# Filtrado por categorías
@movie_router.get('/movies/', tags = ['Movies'], response_model=List[Movie]) 
def get_movies_by_category(category: str = Query(min_length=5, max_length=30)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# # Insertar datos, Crear Registros, NO HAY QUE USAR EL ID EN EL FORMULARIO (porque es autogenerado), borrarlo antes de ejecutar el formulario.
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

# Actualización: Modificando 
@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie)-> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

# Eliminación de registros
@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:
    db = Session()
    result: MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontró"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})