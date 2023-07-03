# Creamos archivo main.py:

from fastapi import FastAPI
from routers import products

app = FastAPI()

# Routers
app.include_router(products.router)

@app.get("/")
# Siempre que llamemos al servidor asimcronamente
async def root():
    return "Hello World"
# # Obtenemos una peticion get para ver una web siempre no con post
@app.get("/url")
# Siempre que llamemos al servidor asimcronamente
async def url():
    return {"url_curso":"https://mouredev.com/python3"}
# Para ver en navegador:
# http://127.0.0.1:8000/user/1
# http://127.0.0.1:8000/user/2
# http://127.0.0.1:8000/user/3
# http://127.0.0.1:8000/user/4#ERROR NO EXISTE USUSARIO
# INICIO CON UVICORN:
# uvicorn main:app --reload
# Vamos con thunderclient:
# http://127.0.0.1:8000/url  VEMOS: {
#   "url_curso": "https://mouredev.com/python3"
# }
# Vamos con thunderclient:
# http://127.0.0.1:8000/products
# Vemos:
# [
#   "Producto1",
#   "Producto2",
#   "Producto3",
#   "Producto4",
#   "Producto5"
# ]
