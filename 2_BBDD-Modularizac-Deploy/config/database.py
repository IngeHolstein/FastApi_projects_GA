import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define el nombre del archivo SQLite
sqlite_file_name = "../database.sqlite"

# Obtiene el directorio actual del archivo en ejecución
base_dir = os.path.dirname(os.path.realpath(__file__))

# Construye la URL de conexión a la base de datos SQLite
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}" 

# En el caso de utilizar postgreSQL
# DATABASE_URL="postgresql+psycopg2://user:pasword@localhost:5432/database_name"

# Crea un motor de base de datos con la URL especificada y habilita la salida de log SQL
engine = create_engine(database_url, echo=True)

# Crea una clase de sesión configurada para utilizar el motor de base de datos
Session = sessionmaker(bind=engine)

# Crea una clase base para las clases de modelo ORM
Base = declarative_base()
