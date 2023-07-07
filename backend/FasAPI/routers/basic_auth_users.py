from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mourede.com",
        "disabled": False,
        "password": "$2b$12$EC.y2xdQY80tnnK85ll4ouLZ7p7nRqN9V4uOh8fiPAK2FGPIxODpC",
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "disabled": True,
        "password": "$2b$12$3WeDpOX6kJqrLVFR5G6nmuD2/hVpTNFhoYNwV9uT4prTdVCTFJxl.",
    },
}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def search_user_db(username: str):
    if username in users_db:
        user_data = users_db[username]
        return UserDB(**user_data)


def authenticate_user(username: str, password: str):
    user = search_user_db(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2)):
    user = search_user_db(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_current_user(user: User = Depends(get_current_user)):
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
 