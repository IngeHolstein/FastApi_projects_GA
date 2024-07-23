from jwt import encode, decode

def create_token(data: dict) -> str:
    token: str = encode(payload=data, key="my_secret_key", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key="my_secret_key", algorithms=['HS256'])
    return data

# Buen video! Pero cuidado con lo que guardan en las tokens!
# La clave secreta es necesaria para verificar que fueron creadas 
# por nuestro server, pero no para ver el contenido que guardan (ya que solo las pasa a base64)
# Páginas como ‘jwt . io’ te enseñan sus componentes:
# # Enlace directo: Descifrar tokens
# https://jwt.io/