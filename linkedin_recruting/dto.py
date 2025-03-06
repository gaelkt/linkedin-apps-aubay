from pydantic import BaseModel # type: ignore
# Modèle pour la requête utilisateur
class UserRequest(BaseModel):
    firstname:str
    lastname:str
    email: str
    password: str 