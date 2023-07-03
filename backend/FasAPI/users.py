from fastapi import FastAPI
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


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except IndexError:
        return {"error": "No se ha encontrado el ususario"}


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
# PONGO y NO ME DA ERROR:
# http://127.0.0.1:8000/userquery?id=1

# VOY POR 2h19 BIEN
