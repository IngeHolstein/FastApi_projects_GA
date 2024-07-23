# Resumen del Curso
# Click Acá para ver el Repositorio
# https://github.com/joelbarranteswins/Platzi-Courses/tree/main/Desarrollo%20Backend%20con%20Python/Curso%20de%20FastAPI%20-%20Path%20Operations%2C%20Validaciones%20y%20Autenticaci%C3%B3n

from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")

class User(BaseModel):
    email:str
    password:str

# También
# app = FastAPI(
#     title= 'Aprendiendo FastApi',
#     description= 'Una API solo por diversión',
#     version= '0.0.1',
# )
# 127.0.0.1:8000/docs

# Iniciamos el servidor
# uvicorn main:app --reload --port 8000

# Si queremos que otros equipos vean la aplicacion desde la red
# uvicorn main:app --reload --port 8000 --host 0.0.0.0
# en la pc cliente http://ip del host:8000/.


# -------------------------------------------------------------------- Creación de Esquemas Y validación de tipo de Datos


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2024)
    rating:float 
    category:str 

    class Config:
        schema_extra = {
                "example": {
                    "id": 1,
                    "title": "Mi película",
                    "overview": "Descripción de la película",
                    "year": 2022,
                    "rating": 9.8,
                    "category" : "Acción"
                }
            }

# Como ahora se va a trabajar con objetos, hay que tener en cuenta 
# que en la lista estábamos trabajando con diccionarios.
# Así que, con los nuevos esquemas al hacer el update genera un error 
# por no ser el mismo tipo el id. Ya pasa a ser de tipo Movie y no dic como veníamos trabajando.
# Una de las soluciones puede ser, guardar la película como 
# un diccionario usando dict()

# @app.post('/movies', tags=['movies'])
# def create_movie(movie: Movie):
#     movie_list.append(movie.dict())
#     return movie
# ------------------------------------------------------------------------------------------
# -------------------------------------------------------------------- Método GET


@app.get('/', tags=['home'])  # Método GET
def message():
    return HTMLResponse('<h1>Hello world</h1>')  # Retornamos HTML

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

# -------------------------------------------------------------------- Parámetros en la Ruta
@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404,content=[])
# ------------------------------------------------------------------------------------------

# -------------------------------------------------------------------- Parámetros Query
# Si no especifíco nada FastApi lo toma como parámetros querys
@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [ item for item in movies if item['category'] == category ]
    return JSONResponse(content=data)
# Un query parameter es un conjunto de parámetros opcionales los cuales son añadidos al
# finalizar la ruta, con el objetivo de definir contenido o acciones en la url, estos
# elementos se añaden después de un ?, para agregar más query parameters utilizamos &.
# ------------------------------------------------------------------------------------------


# -------------------------------------------------------------------- Método POST


@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:  # para que pida todo en el Cuerpo
    # movies.append(movie)
    movies.append(movie.dict())
    return JSONResponse(status_code=201 ,content={"message": "Se ha registrado la película"})
# @app.post('/movies', tags=['movies'])
# def create_movie(movie: Movie):
#     movie_list.append(movie.dict())
#     return movie
# ------------------------------------------------------------------------------------------

# -------------------------------------------------------------------- Método POST
@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200) # Para modificar una película requerimos su Id
def update_movie(id: int, movie: Movie)-> dict:
	for item in movies:
		if item["id"] == id:
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})


@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200 )
def delete_movie(id: int)-> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse( status_code=200, content={"message": "Se ha eliminado la película"})
# ------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------
movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
                "rating": 7.8,
                "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar 2",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
                "rating": 7.8,
                "category": "Acción"
    }
]

# ------------------------------------------------------------------------------------------
# Por defecto FastAPI convierte los valores retornados a JSON, 
# transformando y usando por detras JSONResponse.
# No sería del todo necesario usar JSONResponse si es que no 
# es para un caso especifico.
# https://fastapi.tiangolo.com/advanced/response-directly/
# ------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------
# Flujo de autenticación
# Ahora empezaremos con el módulo de autenticaciones pero antes quiero explicarte un poco 
# acerca de lo que estaremos realizando en nuestra aplicación y cómo será el proceso de 
# autenticación y autorización.

# Ruta para iniciar sesión
# Lo que obtendremos como resultado al final de este módulo es la protección de determinadas 
# rutas de nuestra aplicación para las cuales solo se podrá acceder mediante el inicio de 
# sesión del usuario. Para esto crearemos una ruta que utilice el método POST donde se 
# solicitarán los datos como email y contraseña.

# Creación y envío de token
# Luego de que el usuario ingrese sus datos de sesión correctos este obtendrá un token que le 
# servirá para enviarlo al momento de hacer una petición a una ruta protegida.

# Validación de token
# Al momento de que nuestra API reciba la petición del usuario, comprobará que este le haya 
# enviado el token y validará si es correcto y le pertenece. Finalmente se le dará acceso a 
# la ruta que está solicitando.

# En la siguiente clase empezaremos con la creación de una función que nos va a permitir 
# generar tokens usando la librería pyjwt.
# ------------------------------------------------------------------------------------------


# Como buenas practicas:
# 1- La información contenida en el payload es facilmente detectable, por lo que es 
# importante que no vaya información sencible o podra ser hackeada.

# 2- La llave es gran parte de lo que da la seguridad en jwt, por lo que no 
# debe quedar expuesta en el código y es sano usar un .env depronto con la libreria
# pip install dotenv

# 3- la llave es mejor que no sea tan facil de decifrar por lo que se puede usar

# https://www.allkeysgenerator.com/Random/Security-Encryption-Key-Generator.aspx
# les genera una llave aleatoria y segura en el tamaño y con la encriptación que 
# ustedes decidan