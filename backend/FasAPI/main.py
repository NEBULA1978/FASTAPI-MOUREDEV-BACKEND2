# Creamos archivo main.py:

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
# Siempre que llamemos al servidor asimcronamente
async def root():
    return "Hello World"
# # Obtenemos una peticion get para ver una web siempre no con post
@app.get("/url")
# Siempre que llamemos al servidor asimcronamente
async def url():
    return {"url_curso":"https://mouredev.com/python3"}
