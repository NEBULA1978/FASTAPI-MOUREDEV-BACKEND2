from fastapi import FastAPI

app = FastAPI()


@app.get("/products")
# Siempre que llamemos al servidor asimcronamente
async def products():
    return ["Producto1","Producto2","Producto3","Producto4","Producto5"]

# Para iniciar uvicorn de esta api productos
# uvicorn products:app --reload
# Para ver en thunderclient:
# http://127.0.0.1:8000/products