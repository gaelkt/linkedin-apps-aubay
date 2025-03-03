from pydantic import BaseModel # type: ignore
# Modèle pour la requête utilisateur
class UserRequest(BaseModel):
    username:str
    email: str
    password: str 