# Creamos archivo main.py:

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
# Siempre que llamemos al servidor asimcronamente
async def root():
    return "Hello World"