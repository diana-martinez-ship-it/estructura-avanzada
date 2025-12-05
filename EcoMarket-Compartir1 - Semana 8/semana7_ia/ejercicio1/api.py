"""
API REST de Products - FastAPI
Ejercicio 1: Esqueleto de API + contratos
"""
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from uuid import UUID, uuid4
from datetime import datetime
from typing import Dict
import json

from dtos import (
    CreateProductDTO,
    UpdateProductDTO,
    ListQueryDTO,
    ProductResponseDTO,
    ListResponseDTO,
    DeleteResponseDTO,
    SuccessResponse,
    ErrorResponse,
    ErrorDetail
)

# Configuración de la app
app = FastAPI(
    title="EcoMarket Products API",
    version="1.0.0",
    description="API REST para gestión de productos con validación robusta"
)

# Simulación de BD en memoria
products_db: Dict[UUID, dict] = {}

# Límite de payload (1MB)
MAX_PAYLOAD_SIZE = 1024 * 1024


# ============== MIDDLEWARE ==============

@app.middleware("http")
async def limit_payload_size(request: Request, call_next):
    """Limitar tamaño del payload"""
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_PAYLOAD_SIZE:
        return JSONResponse(
            status_code=413,
            content={
                "data": None,
                "error": {
                    "code": "PAYLOAD_TOO_LARGE",
                    "msg": f"Payload excede el límite de {MAX_PAYLOAD_SIZE} bytes",
                    "details": []
                },
                "meta": {"timestamp": datetime.utcnow().isoformat()}
            }
        )
    return await call_next(request)


# ============== EXCEPTION HANDLERS ==============

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para errores de validación de Pydantic"""
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        details.append(ErrorDetail(
            field=field or None,
            message=error["msg"]
        ))
    
    return JSONResponse(
        status_code=400,
        content={
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "msg": "Datos de entrada inválidos",
                "details": [d.dict() for d in details]
            },
            "meta": {"timestamp": datetime.utcnow().isoformat()}
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler para HTTPException"""
    error_codes = {
        400: "BAD_REQUEST",
        401: "UNAUTHENTICATED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        429: "RATE_LIMITED",
        500: "INTERNAL_ERROR"
    }
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "data": None,
            "error": {
                "code": error_codes.get(exc.status_code, "UNKNOWN_ERROR"),
                "msg": exc.detail,
                "details": []
            },
            "meta": {"timestamp": datetime.utcnow().isoformat()}
        }
    )


# ============== RUTAS ==============

@app.get("/api/v1/products", response_model=ListResponseDTO, tags=["Products"])
async def list_products(
    page: int = 1,
    limit: int = 20,
    currency: str = None,
    min_price: float = None,
    max_price: float = None
):
    """
    Listar productos con paginación y filtros
    """
    # Validar query params
    query = ListQueryDTO(
        page=page,
        limit=limit,
        currency=currency,
        min_price=min_price,
        max_price=max_price
    )
    
    # Filtrar productos
    filtered = list(products_db.values())
    
    if query.currency:
        filtered = [p for p in filtered if p["currency"] == query.currency]
    if query.min_price is not None:
        filtered = [p for p in filtered if p["price"] >= query.min_price]
    if query.max_price is not None:
        filtered = [p for p in filtered if p["price"] <= query.max_price]
    
    # Paginación
    total = len(filtered)
    start = (query.page - 1) * query.limit
    end = start + query.limit
    paginated = filtered[start:end]
    
    return {
        "data": paginated,
        "error": None,
        "meta": {
            "page": query.page,
            "limit": query.limit,
            "total": total,
            "totalPages": (total + query.limit - 1) // query.limit,
            "timestamp": datetime.utcnow().isoformat()
        }
    }


@app.post("/api/v1/products", response_model=SuccessResponse, status_code=201, tags=["Products"])
async def create_product(product: CreateProductDTO):
    """
    Crear un nuevo producto
    """
    product_id = uuid4()
    now = datetime.utcnow()
    
    new_product = {
        "id": product_id,
        "name": product.name,
        "price": product.price,
        "currency": product.currency,
        "tags": product.tags,
        "createdAt": now,
        "updatedAt": now
    }
    
    products_db[product_id] = new_product
    
    return {
        "data": new_product,
        "error": None,
        "meta": {"timestamp": now.isoformat()}
    }


@app.get("/api/v1/products/{product_id}", response_model=SuccessResponse, tags=["Products"])
async def get_product(product_id: UUID):
    """
    Obtener un producto por ID
    """
    if product_id not in products_db:
        raise HTTPException(
            status_code=404,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    
    return {
        "data": products_db[product_id],
        "error": None,
        "meta": {"timestamp": datetime.utcnow().isoformat()}
    }


@app.put("/api/v1/products/{product_id}", response_model=SuccessResponse, tags=["Products"])
async def update_product(product_id: UUID, product: UpdateProductDTO):
    """
    Actualizar un producto existente
    """
    if product_id not in products_db:
        raise HTTPException(
            status_code=404,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    
    existing = products_db[product_id]
    
    # Actualizar solo campos proporcionados
    update_data = product.dict(exclude_unset=True)
    for field, value in update_data.items():
        existing[field] = value
    
    existing["updatedAt"] = datetime.utcnow()
    
    return {
        "data": existing,
        "error": None,
        "meta": {"timestamp": existing["updatedAt"].isoformat()}
    }


@app.delete("/api/v1/products/{product_id}", response_model=DeleteResponseDTO, tags=["Products"])
async def delete_product(product_id: UUID):
    """
    Eliminar un producto
    """
    if product_id not in products_db:
        raise HTTPException(
            status_code=404,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    
    del products_db[product_id]
    
    return {
        "data": {"deleted": True, "id": str(product_id)},
        "error": None,
        "meta": {"timestamp": datetime.utcnow().isoformat()}
    }


@app.get("/", tags=["Health"])
async def root():
    """Health check"""
    return {
        "status": "ok",
        "service": "EcoMarket Products API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
