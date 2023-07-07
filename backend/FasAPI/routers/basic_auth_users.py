from fastapi import FastAPI, Depends,HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenurl="login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


# Una lista o un array
users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mourede.com",
        "disabled": False,
        "password": "123456",
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "disabled": True,
        "password": "654321",
    },
}


def search_user(username: str):
    if username in users_db:
        return UserDB(users_db[username])


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Buscamos usuario en la base de datos
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail=" El ususario no es correcto")
    # Comprobamos usuario base de datos
    user = search_user(form.username)
    # Comprobamos contraseña
    if not form.password == user.password:
            raise HTTPException(
                status_code=400, detail=" La contraseña no es correcta")
    return {"acces_token": user.username,"token_type":"bearer"}


# Para iniciar api autentificacion:
# Aquí en carpeta routers:
# uvicorn basic_auth_users:app --reload
