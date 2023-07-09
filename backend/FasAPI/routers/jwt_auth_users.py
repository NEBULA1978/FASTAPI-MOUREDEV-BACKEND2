from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

ALGORITHMN = "HS256"
# Duration is 1 minute
ACCESS_TOKEN_DURATION = 1
# GENERO  DESDE CONSOLA
# next@rases:~$ openssl rand -hex 23
# f404aaddd22f07be3c526e7f3f6858389c4d2cda15eeb0

SECRET = "f404aaddd22f07be3c526e7f3f6858389c4d2cda15eeb0"

app = FastAPI()

crypt = CryptContext(schemes=["bcrypt"])

# We have an endpoint called "login"
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


# Define user models
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


# User database (dictionary)
users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mourede.com",
        "disabled": False,
        "password": "$2a$12$fcojdAceoKpkkgLBdByvL.s9b.lJYoulzkI4uJjGMwKcsWFHZWjhe",
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "disabled": True,
        "password": "$2a$12$MnV0u2VCMOGRqzSl3hmNSOxj8sphooFsqGqdPx7FrX/.BS8Ul8p3y",
    },
}


# Search user in the database
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):

    user = jwt.decode(token,SECRET,algorithms=ALGORITHMN)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autentificacion invalidas",
            headers={"www-Authenticate": "Bearer"},
        )


async def current_user(user: User = Depends(auth_user)):
    # Si no encontramos usuario excepcion

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ususario inactivo"
        )

    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Search user in the database
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    # Verify the password hash
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")

    # Calculate the expiration time for the access token
    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }

    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHMN),
        "token_type": "bearer",
    }


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


# VOY 5H17
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
