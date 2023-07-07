from fastapi import FastAPI, Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    

    # Si no encontramos usuario excepcion
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autentificacion invalidas",
            headers={"www-Authenticate":"Bearer"})

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ususario inactivo")

    return user
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Buscamos usuario en la base de datos
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail=" El ususario no es correcto")
    # Comprobamos usuario base de datos
    user = search_user_db(form.username)
    # Comprobamos contraseña
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail=" La contraseña no es correcta")
    return {"acces_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


# Para iniciar api autentificacion:
# Aquí en carpeta routers:
# uvicorn basic_auth_users:app --reload
# Para llamar a ruta login con thunderclient en Body con Form enviamos nombre y password;
# Metodo post
# http://127.0.0.1:8000/loginForm Fields
# Form Fields(introducimos valores nombre y password)￼
# username
# mouredev
# ￼
# password

# Peticion GET:
# http://127.0.0.1:8000/users/me
# En Auth en Bearer introducimos en Bearer Token mouredev y nos muestra datos no bien
 