"""
API REST Completa para Testing E2E
===================================

Implementación de /api/v1/products con:
- CRUD completo (Create, Read, Update, Delete)
- Validación robusta
- Manejo de concurrencia (409 Conflict)
- Base de datos en memoria con bloqueo
"""

from fastapi import FastAPI, HTTPException, status, Header
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import datetime
from uuid import uuid4, UUID
import asyncio
from contextlib import asynccontextmanager

# ============== MODELOS ==============

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    price: float = Field(..., ge=0, le=999999999.99)
    currency: str = Field(..., regex="^(MXN|USD|EUR)$")
    tags: Optional[List[str]] = Field(default=[], max_items=10)
    
    @validator('tags')
    def validate_tags(cls, v):
        if v:
            if len(v) != len(set(v)):
                raise ValueError("Tags duplicados no permitidos")
            for tag in v:
                if not tag.islower() or not tag.replace('-', '').isalnum():
                    raise ValueError(f"Tag inválido: {tag}")
        return v
    
    @validator('price')
    def round_price(cls, v):
        return round(v, 2)
    
    @validator('currency')
    def uppercase_currency(cls, v):
        return v.upper()


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=80)
    price: Optional[float] = Field(None, ge=0, le=999999999.99)
    currency: Optional[str] = Field(None, regex="^(MXN|USD|EUR)$")
    tags: Optional[List[str]] = Field(None, max_items=10)
    
    @validator('tags')
    def validate_tags(cls, v):
        if v is not None:
            if len(v) != len(set(v)):
                raise ValueError("Tags duplicados no permitidos")
            for tag in v:
                if not tag.islower() or not tag.replace('-', '').isalnum():
                    raise ValueError(f"Tag inválido: {tag}")
        return v
    
    @validator('price')
    def round_price(cls, v):
        return round(v, 2) if v is not None else None
    
    @validator('currency')
    def uppercase_currency(cls, v):
        return v.upper() if v else None


class Product(BaseModel):
    id: str
    name: str
    price: float
    currency: str
    tags: List[str]
    createdAt: str
    updatedAt: str
    version: int  # Para control de concurrencia optimista


class APIResponse(BaseModel):
    data: Optional[Dict]
    error: Optional[Dict]
    meta: Dict


# ============== BASE DE DATOS EN MEMORIA ==============

class InMemoryDB:
    """Base de datos en memoria con control de concurrencia"""
    
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.locks: Dict[str, asyncio.Lock] = {}  # Lock por producto
        self.global_lock = asyncio.Lock()  # Lock global para operaciones de lista
    
    async def create(self, product_data: ProductCreate) -> Product:
        """Crear nuevo producto"""
        product_id = str(uuid4())
        now = datetime.utcnow().isoformat() + "Z"
        
        product = Product(
            id=product_id,
            name=product_data.name,
            price=product_data.price,
            currency=product_data.currency,
            tags=product_data.tags or [],
            createdAt=now,
            updatedAt=now,
            version=1
        )
        
        async with self.global_lock:
            self.products[product_id] = product
            self.locks[product_id] = asyncio.Lock()
        
        return product
    
    async def get(self, product_id: str) -> Optional[Product]:
        """Obtener producto por ID"""
        return self.products.get(product_id)
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Listar productos con paginación"""
        async with self.global_lock:
            products = list(self.products.values())
        
        # Ordenar por createdAt descendente
        products.sort(key=lambda p: p.createdAt, reverse=True)
        return products[skip:skip + limit]
    
    async def update(self, product_id: str, updates: ProductUpdate, if_match_version: Optional[int] = None) -> Product:
        """Actualizar producto con control de concurrencia optimista"""
        async with self.locks.get(product_id, asyncio.Lock()):
            product = self.products.get(product_id)
            
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail={"code": "NOT_FOUND", "msg": f"Producto {product_id} no encontrado"}
                )
            
            # Control de concurrencia optimista
            if if_match_version is not None:
                if product.version != if_match_version:
                    raise HTTPException(
                        status_code=409,
                        detail={
                            "code": "CONFLICT",
                            "msg": f"Conflicto de versión. Esperado: {if_match_version}, actual: {product.version}",
                            "currentVersion": product.version
                        }
                    )
            
            # Aplicar actualizaciones
            update_data = updates.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(product, field, value)
            
            product.updatedAt = datetime.utcnow().isoformat() + "Z"
            product.version += 1
            
            return product
    
    async def delete(self, product_id: str) -> bool:
        """Eliminar producto"""
        async with self.global_lock:
            if product_id in self.products:
                del self.products[product_id]
                if product_id in self.locks:
                    del self.locks[product_id]
                return True
            return False
    
    async def clear(self):
        """Limpiar toda la base de datos (para tests)"""
        async with self.global_lock:
            self.products.clear()
            self.locks.clear()
    
    async def count(self) -> int:
        """Contar productos"""
        return len(self.products)


# ============== APLICACIÓN FASTAPI ==============

db = InMemoryDB()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle hooks"""
    # Startup
    print("🚀 API iniciada")
    yield
    # Shutdown
    await db.clear()
    print("🛑 API detenida")


app = FastAPI(
    title="Products API",
    version="1.0.0",
    lifespan=lifespan
)


# ============== ENDPOINTS ==============

@app.get("/")
async def root():
    """Health check"""
    return {
        "data": {"status": "healthy", "version": "1.0.0"},
        "error": None,
        "meta": {"timestamp": datetime.utcnow().isoformat() + "Z"}
    }


@app.post("/api/v1/products", status_code=201)
async def create_product(product: ProductCreate):
    """Crear nuevo producto"""
    try:
        created_product = await db.create(product)
        
        return {
            "data": created_product.dict(),
            "error": None,
            "meta": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "requestId": str(uuid4())
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "VALIDATION_ERROR",
                "msg": str(e)
            }
        )


@app.get("/api/v1/products/{product_id}")
async def get_product(product_id: str):
    """Obtener producto por ID"""
    # Validar UUID
    try:
        UUID(product_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_UUID",
                "msg": f"UUID inválido: {product_id}"
            }
        )
    
    product = await db.get(product_id)
    
    if not product:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "msg": f"Producto {product_id} no encontrado"
            }
        )
    
    return {
        "data": product.dict(),
        "error": None,
        "meta": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "requestId": str(uuid4())
        }
    }


@app.get("/api/v1/products")
async def list_products(skip: int = 0, limit: int = 100):
    """Listar productos con paginación"""
    if skip < 0:
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_PARAM", "msg": "skip debe ser >= 0"}
        )
    
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_PARAM", "msg": "limit debe estar entre 1 y 100"}
        )
    
    products = await db.list(skip, limit)
    total = await db.count()
    
    return {
        "data": {
            "items": [p.dict() for p in products],
            "total": total,
            "page": skip // limit + 1,
            "pageSize": limit
        },
        "error": None,
        "meta": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "requestId": str(uuid4())
        }
    }


@app.put("/api/v1/products/{product_id}")
async def update_product(
    product_id: str,
    updates: ProductUpdate,
    if_match: Optional[str] = Header(None)
):
    """Actualizar producto con control de concurrencia optimista"""
    # Validar UUID
    try:
        UUID(product_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_UUID",
                "msg": f"UUID inválido: {product_id}"
            }
        )
    
    # Parsear version desde If-Match header
    if_match_version = None
    if if_match:
        try:
            if_match_version = int(if_match.strip('"'))
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_HEADER",
                    "msg": f"If-Match inválido: {if_match}"
                }
            )
    
    try:
        updated_product = await db.update(product_id, updates, if_match_version)
        
        return {
            "data": updated_product.dict(),
            "error": None,
            "meta": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "requestId": str(uuid4())
            }
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "VALIDATION_ERROR",
                "msg": str(e)
            }
        )


@app.delete("/api/v1/products/{product_id}", status_code=204)
async def delete_product(product_id: str):
    """Eliminar producto"""
    # Validar UUID
    try:
        UUID(product_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_UUID",
                "msg": f"UUID inválido: {product_id}"
            }
        )
    
    deleted = await db.delete(product_id)
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "msg": f"Producto {product_id} no encontrado"
            }
        )
    
    return None  # 204 No Content


# ============== ENDPOINT PARA TESTS ==============

@app.post("/api/v1/_test/clear", status_code=204)
async def clear_database():
    """Limpiar base de datos (solo para tests)"""
    await db.clear()
    return None


@app.get("/api/v1/_test/stats")
async def get_stats():
    """Obtener estadísticas de la base de datos (solo para tests)"""
    return {
        "data": {
            "productCount": await db.count(),
            "lockCount": len(db.locks)
        },
        "error": None,
        "meta": {"timestamp": datetime.utcnow().isoformat() + "Z"}
    }


# ============== EXCEPTION HANDLERS ==============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handler para HTTPException"""
    return {
        "data": None,
        "error": exc.detail if isinstance(exc.detail, dict) else {"code": "ERROR", "msg": str(exc.detail)},
        "meta": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "requestId": str(uuid4())
        }
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handler para excepciones no manejadas"""
    return {
        "data": None,
        "error": {
            "code": "INTERNAL_ERROR",
            "msg": "Error interno del servidor"
        },
        "meta": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "requestId": str(uuid4())
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
