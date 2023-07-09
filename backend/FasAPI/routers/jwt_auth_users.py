from fastapi import FastAPI, Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta

ALGORITHN = "HS256"
# Dura 1 minuto
ACCES_TOKEN_DURATION = 1

app = FastAPI()

crypt = CryptContext(schemes="bcrypt")

# Tenemos endpoint que se llama login
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# PASO1 hacia arriba

# PASO2 hacia abajo
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
        "password": " $2a$12$fcojdAceoKpkkgLBdByvL.s9b.lJYoulzkI4uJjGMwKcsWFHZWjhe ",
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "disabled": True,
        "password": " $2a$12$MnV0u2VCMOGRqzSl3hmNSOxj8sphooFsqGqdPx7FrX/.BS8Ul8p3y ",
    },
}
# Pagina para encriptar contraseñas:
# https://bcrypt-generator.com/

# PASO2 final

# PASO3 Inicio

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Buscamos usuario en la base de datos
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail=" El ususario no es correcto")
    # Comprobamos usuario base de datos
    user = search_user_db(form.username)

    # Verificamos contraseña encriptada
    

    # Comprobamos contraseña
    if not crypt.verify(form.password,user.password):
        raise HTTPException(status_code=400, detail=" La contraseña no es correcta")
    # Tiempo de expiracion
    # access_token_expiration = timedelta(minutes=ACCES_TOKEN_DURATION)

    # El tiempo de ahora mas 1minuto expira

    # Introduzco abajo y elimino la variable
    # expire = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION)

    access_token={"sub":user.username,
                "exp":datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION)} 

    return {"access_token": access_token, "token_type": "bearer"}




# PASO3 Final





# Para iniciar en consola carpeta routers:
# uvicorn jwt_auth_users:app --reload

# Instalo:
# pip install "python-jose[cryptography]"
#  pip install "passlib[bcrypt]"










# ANTERIOR FALLA
# from fastapi import FastAPI, Depends, HTTPException,status,crypt
# from pydantic import BaseModel
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import jwt
# from passlib.context import CryptContext


# ALGORITHN = "HS256"

# app = FastAPI()

# oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Crypt = CryptContext(scheme="bcrypt")

# class User(BaseModel):
#     username: str
#     full_name: str
#     email: str
#     disabled: bool


# class UserDB(User):
#     password: str


# # Una lista o un array
# users_db = {
#     "mouredev": {
#         "username": "mouredev",
#         "full_name": "Brais Moure",
#         "email": "braismoure@mourede.com",
#         "disabled": False,
#         "password": " $2a$12$Lx7XRVYhX.3fK0nQIrGHUeJK82RtOxQu2.eK1GNXXpsrCSAfZ.CIm ",
#     },
#     "mouredev2": {
#         "username": "mouredev2",
#         "full_name": "Brais Moure 2",
#         "email": "braismoure2@mourede.com",
#         "disabled": True,
#         "password": " $2a$12$7Yl5xXBT4r9TZFBqpPFOkOIPiYBD9k/EZ9whHmc9ckP1iN3ilpmii ",
#     },
# }


# def search_user_db(username: str):
#     if username in users_db:
#         return UserDB(**users_db[username])
    

# @app.post("/login")
# async def login(form: OAuth2PasswordRequestForm = Depends()):
#     # Buscamos usuario en la base de datos
#     user_db = users_db.get(form.username)
#     if not user_db:
#         raise HTTPException(status_code=400, detail=" El ususario no es correcto")
#     # Comprobamos usuario base de datos
#     user = search_user_db(form.username)
#     # Comprobamos contraseña
#     if not crypt.verify(form.password,user.password):
#         raise HTTPException(status_code=400, detail=" La contraseña no es correcta")
#     return {"acces_token": user.username, "token_type": "bearer"}

# Empezamos jwt 4H54