from fastapi import FastAPI, Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext


ALGORITHN = "HS256"
crypt = CryptContext(schemes="bcrypt")


app = FastAPI()

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
    # Comprobamos contraseña
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail=" La contraseña no es correcta")
    return {"acces_token": user.username, "token_type": "bearer"}




# PASO3 Final







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