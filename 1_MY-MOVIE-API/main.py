from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi import Body
from fastapi import Path
from fastapi import Query
from fastapi import Request
from fastapi import HTTPException
from fastapi import Depends
from pydantic import BaseModel
from pydantic import Field
from typing import Optional
from typing import List
from jwt_manager import create_token
from jwt_manager import validate_token
from fastapi.security import HTTPBearer


# Creamos Una instancia de FastAPI
app = FastAPI()

# Para cambiar el nombre de la aplicacion
app.title = "Mi aplicación con FastAPI"

# Para cambiar la version de la aplicacion
app.version = "0.0.1"


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")
        
class User(BaseModel):
    email : str
    password : str

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=401, content={"message": "Credenciales inválidas, intente de nuevo"})
    
# Creación de Esquemas
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=15)
    overview: str = Field(default='Descripcion de la película en definición', min_length=5, max_length=50)
    year: int = Field(default=2022, le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=10)

    model_config = { # Modelo de Ejemplo
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Mi Pelicula",
                    "overview": "Descripcion de la pelicula",
                    "year": 2022,
                    "rating": 9.9,
                    "category": "Acción"
                }
            ]
        }
    }

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
@app.get("/", tags=['Home']) # Los tags nos permiten agrupar las rutas
def función_root():
    return  HTMLResponse('<h2>Hola mundo usando HTML</h2>')


# Indicamos la Ruta , obtenemos todas las películas
@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)


# Utilizaremos parámetros para seleccionar peleículas por ID
@app.get('/movies/{id}', tags=['Movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content={"message": "Pelicula inexistente"})


@app.get('/movies/', tags = ['Movies'], response_model=List[Movie]) # Filtrado por categorías
def get_movies_by_category(category: str = Query(min_length=5, max_length=30)) -> List[Movie]:
    data = list(filter(lambda item: item['category'] == category , movies))
    return JSONResponse(content=[data])



@app.post('/movies', tags=['Movies'], response_model = dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie.model_dump())
    return JSONResponse(content={"message": "Se ha registrado la película exitosamente"})
    '''
    Body() le dice a FastAPI que estos parámetros se esperan en el cuerpo de la solicitud en formato JSON.
    Por ejemplo, si se envía una solicitud con el cuerpo:
    {
        "id": 1,
        "title": "Inception",
        "overview": "A thief who steals corporate secrets...",
        "year": 2010,
        "rating": 8.8,
        "category": "Sci-Fi"
    }
    FastAPI extraerá estos valores y los asignará a los correspondientes parámetros de la función.
    '''


@app.put('/movies/{id}', tags=['Movies'], response_model = dict,  status_code=200) # Modificando Actualizando
def update_movie(id: int, movie: Movie) -> dict:
	for item in movies:
		if item["id"] == id:
            # Asignación de Variables de la Película
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return JSONResponse(content={"message": "Se ha Actualizado la película exitosamente"})


@app.delete('/movies/{id}', tags=['Movies'], response_model = dict, status_code=200)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message": "Se ha Eliminado la película exitosamente"})