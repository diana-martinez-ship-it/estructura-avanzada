"""
API REST con Observabilidad Completa - Ejercicio 5
Features:
- Logging estructurado JSON con correlationId
- Métricas de latencia (p50, p95, p99) por endpoint
- Contadores de errores (4xx, 5xx) por endpoint
- Request tracing (pipeline completo)
- Middleware de instrumentación automática
"""

import json
import time
import uuid
import logging
from collections import defaultdict, deque
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
import uvicorn


# ============================================================================
# OBSERVABILITY: Logging Estructurado
# ============================================================================

class StructuredLogger:
    """Logger con formato JSON estructurado para observabilidad."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Handler para stdout con formato JSON
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(self._json_formatter())
            self.logger.addHandler(handler)
    
    def _json_formatter(self):
        """Formatter personalizado que emite JSON."""
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    "ts": datetime.utcnow().isoformat() + "Z",
                    "level": record.levelname,
                    "logger": record.name,
                    "msg": record.getMessage(),
                }
                
                # Agregar campos extras del record
                if hasattr(record, 'correlationId'):
                    log_data['correlationId'] = record.correlationId
                if hasattr(record, 'path'):
                    log_data['path'] = record.path
                if hasattr(record, 'method'):
                    log_data['method'] = record.method
                if hasattr(record, 'status'):
                    log_data['status'] = record.status
                if hasattr(record, 'latency_ms'):
                    log_data['latency_ms'] = record.latency_ms
                if hasattr(record, 'userId'):
                    log_data['userId'] = record.userId
                if hasattr(record, 'error'):
                    log_data['error'] = record.error
                
                return json.dumps(log_data)
        
        return JSONFormatter()
    
    def info(self, msg: str, **kwargs):
        self.logger.info(msg, extra=kwargs)
    
    def warning(self, msg: str, **kwargs):
        self.logger.warning(msg, extra=kwargs)
    
    def error(self, msg: str, **kwargs):
        self.logger.error(msg, extra=kwargs)


# Logger global
logger = StructuredLogger("api_observable")


# ============================================================================
# OBSERVABILITY: Métricas
# ============================================================================

class MetricsCollector:
    """Colector de métricas para latencia y errores por endpoint."""
    
    def __init__(self):
        # Latencias: Dict[endpoint, deque[latency_ms]]
        self._latencies: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        
        # Contadores de errores: Dict[endpoint, Dict[status_code, count]]
        self._error_counts: Dict[str, Dict[int, int]] = defaultdict(lambda: defaultdict(int))
        
        # Request count total
        self._request_counts: Dict[str, int] = defaultdict(int)
        
        # Timestamp de inicio
        self.start_time = time.time()
    
    def record_request(self, endpoint: str, latency_ms: float, status_code: int):
        """Registra una request completa."""
        self._request_counts[endpoint] += 1
        self._latencies[endpoint].append(latency_ms)
        
        # Si es error (4xx o 5xx), incrementar contador
        if status_code >= 400:
            self._error_counts[endpoint][status_code] += 1
    
    def get_latency_percentiles(self, endpoint: str) -> Dict[str, float]:
        """Calcula p50, p95, p99 para un endpoint."""
        latencies = sorted(self._latencies.get(endpoint, []))
        
        if not latencies:
            return {"p50": 0.0, "p95": 0.0, "p99": 0.0, "count": 0}
        
        count = len(latencies)
        
        def percentile(p: float) -> float:
            idx = int(count * p / 100)
            return latencies[min(idx, count - 1)]
        
        return {
            "p50": round(percentile(50), 2),
            "p95": round(percentile(95), 2),
            "p99": round(percentile(99), 2),
            "count": count
        }
    
    def get_error_rate(self, endpoint: str) -> Dict[str, Any]:
        """Calcula tasa de error 4xx y 5xx."""
        total = self._request_counts.get(endpoint, 0)
        
        if total == 0:
            return {"error_rate_4xx": 0.0, "error_rate_5xx": 0.0, "total": 0}
        
        errors = self._error_counts.get(endpoint, {})
        
        count_4xx = sum(count for code, count in errors.items() if 400 <= code < 500)
        count_5xx = sum(count for code, count in errors.items() if 500 <= code < 600)
        
        return {
            "error_rate_4xx": round((count_4xx / total) * 100, 2),
            "error_rate_5xx": round((count_5xx / total) * 100, 2),
            "total": total,
            "errors_4xx": count_4xx,
            "errors_5xx": count_5xx
        }
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Retorna todas las métricas de todos los endpoints."""
        metrics = {}
        
        all_endpoints = set(self._request_counts.keys()) | set(self._latencies.keys())
        
        for endpoint in all_endpoints:
            metrics[endpoint] = {
                "latency": self.get_latency_percentiles(endpoint),
                "errors": self.get_error_rate(endpoint)
            }
        
        # Métricas globales
        total_requests = sum(self._request_counts.values())
        uptime_seconds = int(time.time() - self.start_time)
        
        metrics["_global"] = {
            "total_requests": total_requests,
            "uptime_seconds": uptime_seconds,
            "requests_per_second": round(total_requests / max(uptime_seconds, 1), 2)
        }
        
        return metrics


# Collector global
metrics = MetricsCollector()


# ============================================================================
# OBSERVABILITY: Request Tracing
# ============================================================================

class RequestTracer:
    """Trazador de pipeline request→response."""
    
    def __init__(self, correlation_id: str):
        self.correlation_id = correlation_id
        self.steps: List[Dict[str, Any]] = []
        self.start_time = time.perf_counter()
    
    def add_step(self, name: str, details: Optional[Dict] = None):
        """Agrega un paso al trace."""
        elapsed_ms = (time.perf_counter() - self.start_time) * 1000
        
        step = {
            "step": name,
            "timestamp_ms": round(elapsed_ms, 2),
            "details": details or {}
        }
        
        self.steps.append(step)
        
        logger.info(
            f"Trace step: {name}",
            correlationId=self.correlation_id,
            step=name,
            elapsed_ms=round(elapsed_ms, 2)
        )
    
    def get_trace(self) -> List[Dict]:
        """Retorna el trace completo."""
        return self.steps


# ============================================================================
# MODELS (mismo del ejercicio anterior)
# ============================================================================

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    price: Decimal = Field(..., ge=0, decimal_places=2)
    currency: str = Field(..., pattern="^(USD|EUR|MXN)$")
    tags: List[str] = Field(default_factory=list, max_length=10)
    
    @field_validator("price", mode="before")
    def round_price(cls, v):
        if isinstance(v, (int, float, Decimal)):
            return round(Decimal(str(v)), 2)
        return v
    
    @field_validator("currency", mode="before")
    def uppercase_currency(cls, v):
        if isinstance(v, str):
            return v.upper()
        return v
    
    @field_validator("tags", mode="after")
    def unique_tags(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("Tags must be unique")
        return v


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=80)
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    currency: Optional[str] = Field(None, pattern="^(USD|EUR|MXN)$")
    tags: Optional[List[str]] = Field(None, max_length=10)
    
    @field_validator("price", mode="before")
    def round_price(cls, v):
        if v is not None and isinstance(v, (int, float, Decimal)):
            return round(Decimal(str(v)), 2)
        return v
    
    @field_validator("currency", mode="before")
    def uppercase_currency(cls, v):
        if v is not None and isinstance(v, str):
            return v.upper()
        return v
    
    @field_validator("tags", mode="after")
    def unique_tags(cls, v):
        if v is not None and len(v) != len(set(v)):
            raise ValueError("Tags must be unique")
        return v


class Product(BaseModel):
    id: uuid.UUID
    name: str
    price: Decimal
    currency: str
    tags: List[str]
    version: int
    created_at: datetime
    updated_at: datetime


# ============================================================================
# DATABASE (In-Memory)
# ============================================================================

class InMemoryDB:
    def __init__(self):
        self._products: Dict[uuid.UUID, Product] = {}
    
    def create(self, data: ProductCreate) -> Product:
        product_id = uuid.uuid4()
        now = datetime.utcnow()
        
        product = Product(
            id=product_id,
            name=data.name,
            price=data.price,
            currency=data.currency,
            tags=data.tags,
            version=1,
            created_at=now,
            updated_at=now
        )
        
        self._products[product_id] = product
        return product
    
    def get(self, product_id: uuid.UUID) -> Optional[Product]:
        return self._products.get(product_id)
    
    def list_all(self, skip: int = 0, limit: int = 100) -> tuple[List[Product], int]:
        products_list = list(self._products.values())
        total = len(products_list)
        return products_list[skip:skip+limit], total
    
    def update(self, product_id: uuid.UUID, data: ProductUpdate, expected_version: Optional[int] = None) -> Product:
        product = self._products.get(product_id)
        
        if not product:
            return None
        
        # Optimistic locking
        if expected_version is not None and product.version != expected_version:
            raise ValueError(f"Version conflict: expected {expected_version}, got {product.version}")
        
        # Actualizar campos
        update_data = data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(product, field, value)
        
        product.version += 1
        product.updated_at = datetime.utcnow()
        
        return product
    
    def delete(self, product_id: uuid.UUID) -> bool:
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False
    
    def clear(self):
        self._products.clear()
    
    def count(self) -> int:
        return len(self._products)


db = InMemoryDB()


# ============================================================================
# MIDDLEWARE: Observability Instrumentation
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("API starting up", service="api_observable", version="1.0.0")
    yield
    logger.info("API shutting down", total_requests=sum(metrics._request_counts.values()))


app = FastAPI(title="Observable API", version="1.0.0", lifespan=lifespan)


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    """Middleware que instrumenta TODAS las requests."""
    
    # 1. Generar correlationId
    correlation_id = str(uuid.uuid4())
    request.state.correlation_id = correlation_id
    
    # 2. Crear tracer
    tracer = RequestTracer(correlation_id)
    request.state.tracer = tracer
    
    tracer.add_step("request_received", {
        "method": request.method,
        "path": request.url.path,
        "client_ip": request.client.host
    })
    
    # 3. Medir latencia
    start_time = time.perf_counter()
    
    # Log de inicio
    logger.info(
        "Request started",
        correlationId=correlation_id,
        method=request.method,
        path=request.url.path,
        userId=request.headers.get("X-User-Id")  # Simulado
    )
    
    # 4. Ejecutar request
    try:
        tracer.add_step("processing_request")
        response = await call_next(request)
        tracer.add_step("response_generated", {"status": response.status_code})
    
    except Exception as e:
        tracer.add_step("error_occurred", {"error": str(e)})
        
        logger.error(
            "Request failed with exception",
            correlationId=correlation_id,
            method=request.method,
            path=request.url.path,
            error=str(e)
        )
        
        response = JSONResponse(
            status_code=500,
            content={
                "data": None,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "msg": "Internal server error"
                }
            }
        )
    
    # 5. Calcular latencia
    latency_ms = (time.perf_counter() - start_time) * 1000
    tracer.add_step("request_completed", {"latency_ms": round(latency_ms, 2)})
    
    # 6. Registrar métricas
    endpoint = f"{request.method} {request.url.path}"
    metrics.record_request(endpoint, latency_ms, response.status_code)
    
    # 7. Log de finalización
    logger.info(
        "Request completed",
        correlationId=correlation_id,
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        latency_ms=round(latency_ms, 2),
        userId=request.headers.get("X-User-Id")
    )
    
    # 8. Agregar headers de observabilidad
    response.headers["X-Correlation-Id"] = correlation_id
    response.headers["X-Latency-Ms"] = str(round(latency_ms, 2))
    
    return response


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
def health_check(request: Request):
    """Health check endpoint."""
    request.state.tracer.add_step("health_check_executed")
    
    return {
        "data": {
            "status": "healthy",
            "version": "1.0.0",
            "correlationId": request.state.correlation_id
        },
        "error": None
    }


@app.post("/api/v1/products", status_code=201)
def create_product(data: ProductCreate, request: Request):
    """Crea un nuevo producto."""
    tracer = request.state.tracer
    
    tracer.add_step("validating_input", {"name": data.name})
    
    product = db.create(data)
    
    tracer.add_step("product_created", {"product_id": str(product.id)})
    
    logger.info(
        "Product created",
        correlationId=request.state.correlation_id,
        product_id=str(product.id),
        name=product.name
    )
    
    return {
        "data": product.model_dump(mode="json"),
        "error": None
    }


@app.get("/api/v1/products/{product_id}")
def get_product(product_id: uuid.UUID, request: Request):
    """Obtiene un producto por ID."""
    tracer = request.state.tracer
    
    tracer.add_step("querying_database", {"product_id": str(product_id)})
    
    product = db.get(product_id)
    
    if not product:
        tracer.add_step("product_not_found")
        
        logger.warning(
            "Product not found",
            correlationId=request.state.correlation_id,
            product_id=str(product_id)
        )
        
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "msg": f"Product {product_id} not found"
            }
        )
    
    tracer.add_step("product_found", {"name": product.name})
    
    return {
        "data": product.model_dump(mode="json"),
        "error": None
    }


@app.get("/api/v1/products")
def list_products(skip: int = 0, limit: int = 100, request: Request = None):
    """Lista todos los productos con paginación."""
    tracer = request.state.tracer
    
    if skip < 0:
        tracer.add_step("invalid_pagination", {"skip": skip})
        raise HTTPException(status_code=400, detail={"code": "INVALID_SKIP", "msg": "skip must be >= 0"})
    
    if limit < 1 or limit > 100:
        tracer.add_step("invalid_pagination", {"limit": limit})
        raise HTTPException(status_code=400, detail={"code": "INVALID_LIMIT", "msg": "limit must be 1-100"})
    
    tracer.add_step("querying_products_list", {"skip": skip, "limit": limit})
    
    products, total = db.list_all(skip, limit)
    
    tracer.add_step("products_retrieved", {"count": len(products), "total": total})
    
    return {
        "data": {
            "items": [p.model_dump(mode="json") for p in products],
            "total": total,
            "skip": skip,
            "limit": limit
        },
        "error": None
    }


@app.put("/api/v1/products/{product_id}")
def update_product(product_id: uuid.UUID, data: ProductUpdate, request: Request):
    """Actualiza un producto."""
    tracer = request.state.tracer
    
    if_match = request.headers.get("If-Match")
    expected_version = int(if_match.strip('"')) if if_match else None
    
    tracer.add_step("updating_product", {"product_id": str(product_id), "expected_version": expected_version})
    
    try:
        product = db.update(product_id, data, expected_version)
    except ValueError as e:
        tracer.add_step("version_conflict", {"error": str(e)})
        
        logger.warning(
            "Version conflict",
            correlationId=request.state.correlation_id,
            product_id=str(product_id),
            error=str(e)
        )
        
        raise HTTPException(
            status_code=409,
            detail={
                "code": "CONFLICT",
                "msg": str(e)
            }
        )
    
    if not product:
        tracer.add_step("product_not_found")
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "msg": f"Product {product_id} not found"})
    
    tracer.add_step("product_updated", {"new_version": product.version})
    
    logger.info(
        "Product updated",
        correlationId=request.state.correlation_id,
        product_id=str(product_id),
        new_version=product.version
    )
    
    return {
        "data": product.model_dump(mode="json"),
        "error": None
    }


@app.delete("/api/v1/products/{product_id}", status_code=204)
def delete_product(product_id: uuid.UUID, request: Request):
    """Elimina un producto."""
    tracer = request.state.tracer
    
    tracer.add_step("deleting_product", {"product_id": str(product_id)})
    
    deleted = db.delete(product_id)
    
    if not deleted:
        tracer.add_step("product_not_found")
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "msg": f"Product {product_id} not found"})
    
    tracer.add_step("product_deleted")
    
    logger.info(
        "Product deleted",
        correlationId=request.state.correlation_id,
        product_id=str(product_id)
    )
    
    return Response(status_code=204)


# ============================================================================
# OBSERVABILITY ENDPOINTS
# ============================================================================

@app.get("/api/v1/_metrics")
def get_metrics(request: Request):
    """Retorna todas las métricas recolectadas."""
    tracer = request.state.tracer
    
    tracer.add_step("retrieving_metrics")
    
    all_metrics = metrics.get_all_metrics()
    
    tracer.add_step("metrics_retrieved", {"endpoints_count": len(all_metrics) - 1})
    
    return {
        "data": all_metrics,
        "error": None
    }


@app.get("/api/v1/_trace")
def get_trace(request: Request):
    """Retorna el trace de la request actual."""
    tracer = request.state.tracer
    
    tracer.add_step("retrieving_trace")
    
    trace = tracer.get_trace()
    
    return {
        "data": {
            "correlationId": request.state.correlation_id,
            "steps": trace
        },
        "error": None
    }


@app.post("/api/v1/_test/clear", status_code=204)
def clear_database(request: Request):
    """Limpia la base de datos (solo para tests)."""
    request.state.tracer.add_step("clearing_database")
    
    db.clear()
    
    logger.info("Database cleared", correlationId=request.state.correlation_id)
    
    return Response(status_code=204)


@app.get("/api/v1/_test/stats")
def get_stats(request: Request):
    """Retorna estadísticas de la base de datos."""
    request.state.tracer.add_step("retrieving_stats")
    
    return {
        "data": {
            "productCount": db.count()
        },
        "error": None
    }


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler para HTTPException con logging."""
    
    logger.warning(
        "HTTP exception",
        correlationId=request.state.correlation_id,
        status=exc.status_code,
        error=str(exc.detail)
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "data": None,
            "error": exc.detail if isinstance(exc.detail, dict) else {"code": "ERROR", "msg": str(exc.detail)}
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para excepciones no capturadas."""
    
    logger.error(
        "Unhandled exception",
        correlationId=request.state.correlation_id,
        error=str(exc),
        error_type=type(exc).__name__
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "data": None,
            "error": {
                "code": "INTERNAL_ERROR",
                "msg": "Internal server error"
            }
        }
    )


if __name__ == "__main__":
    uvicorn.run("api_observable:app", host="0.0.0.0", port=8000, reload=True)
