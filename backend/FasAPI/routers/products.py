from fastapi import APIRouter

router = APIRouter(prefix="/products")

product_list = ["Producto1","Producto2","Producto3","Producto4","Producto5"]


@router.get("/products")
# Siempre que llamemos al servidor asimcronamente
async def products():
    return product_list

@router.get("/products/{id}")
# Siempre que llamemos al servidor asimcronamente
async def products(id: int):
    return product_list
# Para iniciar uvicorn de esta api productos
# uvicorn products:app --reload
# Para ver en thunderclient:
# http://127.0.0.1:8000/products
# Para ver en thunderclient:
# http://127.0.0.1:8000/users Vemos ususarios con router