"""
DTOs para API de Products - Ejercicio 1
Validación con Pydantic (JSON Schema automático)
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from enum import Enum


class Currency(str, Enum):
    """Monedas soportadas"""
    MXN = "MXN"
    USD = "USD"
    EUR = "EUR"


# ============== REQUEST DTOs ==============

class CreateProductDTO(BaseModel):
    """DTO para crear un producto"""
    name: str = Field(..., min_length=2, max_length=80, description="Nombre del producto")
    price: float = Field(..., ge=0, description="Precio >= 0")
    currency: Currency = Field(default=Currency.MXN, description="Moneda")
    tags: List[str] = Field(default_factory=list, max_items=10, description="Máximo 10 tags")
    
    @validator('name')
    def sanitize_name(cls, v):
        """Sanitización básica XSS"""
        dangerous = ['<script>', '</script>', '<iframe>', 'javascript:', 'onerror=']
        for pattern in dangerous:
            if pattern.lower() in v.lower():
                raise ValueError(f"Patrón sospechoso detectado: {pattern}")
        return v.strip()
    
    @validator('tags')
    def sanitize_tags(cls, v):
        """Sanitizar tags"""
        return [tag.strip()[:50] for tag in v if tag.strip()]
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Laptop Ecológica",
                "price": 899.99,
                "currency": "MXN",
                "tags": ["tecnología", "sostenible"]
            }
        }


class UpdateProductDTO(BaseModel):
    """DTO para actualizar un producto (campos opcionales)"""
    name: Optional[str] = Field(None, min_length=2, max_length=80)
    price: Optional[float] = Field(None, ge=0)
    currency: Optional[Currency] = None
    tags: Optional[List[str]] = Field(None, max_items=10)
    
    @validator('name')
    def sanitize_name(cls, v):
        if v:
            dangerous = ['<script>', '</script>', '<iframe>', 'javascript:', 'onerror=']
            for pattern in dangerous:
                if pattern.lower() in v.lower():
                    raise ValueError(f"Patrón sospechoso detectado: {pattern}")
            return v.strip()
        return v


class ListQueryDTO(BaseModel):
    """Query params para listar productos"""
    page: int = Field(default=1, ge=1, description="Página (>=1)")
    limit: int = Field(default=20, ge=1, le=100, description="Límite por página (1-100)")
    currency: Optional[Currency] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)


# ============== RESPONSE DTOs ==============

class ProductResponseDTO(BaseModel):
    """DTO de respuesta para un producto"""
    id: UUID
    name: str
    price: float
    currency: Currency
    tags: List[str]
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        # Orden consistente de propiedades
        fields = {
            'id': {'order': 1},
            'name': {'order': 2},
            'price': {'order': 3},
            'currency': {'order': 4},
            'tags': {'order': 5},
            'createdAt': {'order': 6},
            'updatedAt': {'order': 7},
        }
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Laptop Ecológica",
                "price": 899.99,
                "currency": "MXN",
                "tags": ["tecnología", "sostenible"],
                "createdAt": "2025-11-18T12:00:00Z",
                "updatedAt": "2025-11-18T12:00:00Z"
            }
        }


class ErrorDetail(BaseModel):
    """Detalle de error individual"""
    field: Optional[str] = None
    message: str


class ErrorResponse(BaseModel):
    """Estructura de error estandarizada"""
    code: str
    msg: str
    details: List[ErrorDetail] = []


class SuccessResponse(BaseModel):
    """Respuesta exitosa genérica"""
    data: Optional[dict] = None
    error: Optional[ErrorResponse] = None
    meta: dict = {}
    
    class Config:
        schema_extra = {
            "example_success": {
                "data": {"id": "550e8400-e29b-41d4-a716-446655440000", "name": "Producto"},
                "error": None,
                "meta": {"timestamp": "2025-11-18T12:00:00Z"}
            },
            "example_error": {
                "data": None,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "msg": "Datos de entrada inválidos",
                    "details": [
                        {"field": "price", "message": "El precio debe ser >= 0"}
                    ]
                },
                "meta": {"timestamp": "2025-11-18T12:00:00Z"}
            }
        }


class ListResponseDTO(BaseModel):
    """Respuesta para listar productos"""
    data: List[ProductResponseDTO]
    error: Optional[ErrorResponse] = None
    meta: dict = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Laptop Ecológica",
                        "price": 899.99,
                        "currency": "MXN",
                        "tags": ["tecnología"],
                        "createdAt": "2025-11-18T12:00:00Z",
                        "updatedAt": "2025-11-18T12:00:00Z"
                    }
                ],
                "error": None,
                "meta": {
                    "page": 1,
                    "limit": 20,
                    "total": 1,
                    "totalPages": 1
                }
            }
        }


class DeleteResponseDTO(BaseModel):
    """Respuesta para eliminación"""
    data: dict = {"deleted": True}
    error: Optional[ErrorResponse] = None
    meta: dict = {}


# ============== EJEMPLOS DE VALIDACIÓN ==============

# ✅ VÁLIDO
valid_create = {
    "name": "Mouse Bambú",
    "price": 25.50,
    "currency": "USD",
    "tags": ["tecnología", "eco-friendly"]
}

# ❌ INVÁLIDO - Precio negativo
invalid_price = {
    "name": "Producto",
    "price": -10,
    "currency": "MXN",
    "tags": []
}

# ❌ INVÁLIDO - Nombre muy corto
invalid_name = {
    "name": "A",
    "price": 100,
    "currency": "EUR",
    "tags": []
}

# ❌ INVÁLIDO - Demasiados tags
invalid_tags = {
    "name": "Producto con muchos tags",
    "price": 50,
    "currency": "MXN",
    "tags": [f"tag{i}" for i in range(15)]  # Más de 10
}

# ❌ INVÁLIDO - XSS attempt
invalid_xss = {
    "name": "Producto <script>alert('xss')</script>",
    "price": 100,
    "currency": "MXN",
    "tags": []
}

# ❌ INVÁLIDO - Moneda inexistente
invalid_currency = {
    "name": "Producto",
    "price": 100,
    "currency": "GBP",  # No está en el enum
    "tags": []
}
