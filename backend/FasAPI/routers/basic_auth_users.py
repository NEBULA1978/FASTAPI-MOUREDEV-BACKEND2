from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


# Una lista o un array
users_db = {
    "mouredev":{
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mourede.com",
        "disabled": False,
        "password":"123456"
    },
    "mouredev2":{
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "disabled": True,
        "password":"654321"
    }
}

def search_user(username:str):
    if username in users_db:
        return UserDB(users_db[username])


# Para iniciar api autentificacion:
# Aquí en carpeta routers:
# uvicorn basic_auth_users:app --reload
