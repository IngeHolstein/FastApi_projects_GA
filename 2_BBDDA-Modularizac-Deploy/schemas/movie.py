from pydantic import BaseModel, Field
from typing import Optional, List

# Creación de Esquemas
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=15)
    overview: str = Field(default='Descripcion de la película en definición', min_length=5, max_length=50)
    year: int = Field(default=2022, le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=20)

    model_config = { # Modelo de Ejemplo
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Mi Pelicula",
                    "overview": "Descripcion de la pelicula",
                    "year": 2022,
                    "rating": 8.9,
                    "category": "Acción"
                }
            ]
        }
    }

