from fastapi import FastAPI,HTTPException
from pydantic import BaseModel


app = FastAPI()


class User(BaseModel):
    id: int  # Add the id attribute
    name: str
    surname: str
    url: str
    age: int


users_list = [
    User(
        id=1, name="Jose", surname="Pascual", url="https://mouredev.com/python3", age=35
    ),
    User(id=2, name="Luis", surname="Ivarra", url="https://Ivarra.com/python3", age=25),
    User(
        id=3, name="Pedro", surname="Suarez", url="https://Suarez.com/python3", age=55
    ),
]


@app.get("/usersjson")
async def usersjson():
    return [
        {
            "id": 1,
            "name": "Jose",
            "surname": "Pascual",
            "url": "https://mouredev.com/python3",
            "age": 35,
        },
        {
            "id": 2,
            "name": "Luis",
            "surname": "Ivarra",
            "url": "https://Ivarra.com/python3",
            "age": 25,
        },
        {
            "id": 3,
            "name": "Pedro",
            "surname": "Suarez",
            "url": "https://Suarez.com/python3",
            "age": 55,
        },
    ]


@app.get("/users")
async def users():
    return users_list


@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)


@app.get("/userquery/")
async def user(id: int):
    return search_user(id)


# Para hacer peticion con post en thunderclient:
# http://127.0.0.1:8000/user/
# En el body introduzco json:
# {
#     "id": 4,
#     "name": "Jose",
#     "surname": "Pascual",
#     "url": "https://mouredev.com/python3",
#     "age": 35
# }
# Si lo tengo me dice metodo no permitido


@app.post("/user/",status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204,detail=" El ususario ya existe")
        

    # Si no existe añadimos ususario
    users_list.append(user)
    return user


# Metodo PUT:
# En thundderclient
# http://127.0.0.1:8000/user
# Ymodificamos el valor del json desde el body
@app.put("/user/")
async def user(user: User):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "No se ha actualizado el ususario"}

    return user


# DELETE
# En thunder client
# http://127.0.0.1:8000/user/4

@app.delete("/user/{id}")
async def user(id: int):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error": "No se ha encontrado el ususario"}

    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except IndexError:
        return {"error": "No se ha encontrado el ususario"}
        found = True


# ERROR POR CONSOLA THUNDERCLIENT
# {
#   "detail": [
#     {
#       "loc": [
#         "query",
#         "id"
#       ],
#       "msg": "field required",
#       "type": "value_error.missing"
#     }
#   ]
# }

# En esta ruta absoluta pongo en la consola: uvicorn users:app --reload
# /home/next/Vídeos/VIDEOS_PROYECTOS/FASTAPI-MOUREDEV-BACKEND/backend/FasAPI
# PONGO y NO ME DA ERROR:
# http://127.0.0.1:8000/userquery?id=1

# VOY POR 2h19 BIEN
# VOY POR 2h58 DELETE BIEN
# VOY POR 3h19 DELETE statuscode BIEN
