"""
Middleware de Autenticación y Rate Limiting - Ejercicio 2
FastAPI con JWT, RBAC y Rate Limiting
"""
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import jwt
import time
import uuid
from datetime import datetime, timedelta
from collections import defaultdict
import json

# Configuración
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Almacenamiento en memoria (usar Redis en producción)
refresh_tokens_db: Dict[str, dict] = {}
rate_limit_storage: Dict[str, List[float]] = defaultdict(list)
metrics_storage: Dict[str, dict] = defaultdict(lambda: {
    "count": 0,
    "latencies": [],
    "status_4xx": 0,
    "status_5xx": 0
})

# ============== MODELOS ==============

class UserRole(str):
    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    userId: str
    username: str
    role: str  # "admin" o "user"


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    accessToken: str
    expiresIn: int


class ErrorResponse(BaseModel):
    code: str
    msg: str
    details: List[dict] = []


# Base de datos simulada de usuarios
USERS_DB = {
    "admin": {"userId": "1", "username": "admin", "password": "admin123", "role": UserRole.ADMIN},
    "user1": {"userId": "2", "username": "user1", "password": "user123", "role": UserRole.USER},
}


# ============== UTILIDADES JWT ==============

def create_access_token(data: dict) -> str:
    """Crear JWT con expiración de 15 minutos"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "iss": "ecomarket-api"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Crear refresh token único"""
    token = str(uuid.uuid4())
    refresh_tokens_db[token] = {
        "userId": user_id,
        "createdAt": datetime.utcnow(),
        "expiresAt": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    }
    return token


def verify_token(token: str) -> dict:
    """Verificar y decodificar JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expirado"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )


# ============== MIDDLEWARE 1: CORRELATION ID ==============

async def correlation_id_middleware(request: Request, call_next):
    """Agrega correlation ID único a cada request"""
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    request.state.correlation_id = correlation_id
    
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response


# ============== MIDDLEWARE 2: RATE LIMITING ==============

def check_rate_limit(key: str, limit: int, window: int = 900) -> tuple[bool, dict]:
    """
    Verifica rate limit con sliding window
    Args:
        key: Identificador (IP o userId)
        limit: Número máximo de requests
        window: Ventana de tiempo en segundos (default: 15min = 900s)
    Returns:
        (is_allowed, rate_limit_info)
    """
    current_time = time.time()
    window_start = current_time - window
    
    # Limpiar requests antiguos
    rate_limit_storage[key] = [
        req_time for req_time in rate_limit_storage[key]
        if req_time > window_start
    ]
    
    current_count = len(rate_limit_storage[key])
    remaining = max(0, limit - current_count)
    reset_time = int(current_time + window)
    
    rate_limit_info = {
        "limit": limit,
        "remaining": remaining,
        "reset": reset_time
    }
    
    if current_count >= limit:
        return False, rate_limit_info
    
    # Registrar request actual
    rate_limit_storage[key].append(current_time)
    return True, rate_limit_info


async def rate_limiting_middleware(request: Request, call_next):
    """Rate limiting por IP y userId"""
    
    # Rate limit por IP
    client_ip = request.client.host
    ip_allowed, ip_info = check_rate_limit(f"ip:{client_ip}", limit=100)
    
    if not ip_allowed:
        return JSONResponse(
            status_code=429,
            content={
                "data": None,
                "error": {
                    "code": "RATE_LIMITED",
                    "msg": "Límite de requests por IP excedido (100 req/15min)",
                    "details": []
                },
                "meta": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "rateLimit": ip_info
                }
            },
            headers={
                "X-RateLimit-Limit": str(ip_info["limit"]),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(ip_info["reset"]),
                "Retry-After": "300"
            }
        )
    
    # Ejecutar request
    response = await call_next(request)
    
    # Rate limit por userId (si está autenticado)
    if hasattr(request.state, "user"):
        user_id = request.state.user["userId"]
        user_allowed, user_info = check_rate_limit(f"user:{user_id}", limit=1000)
        
        if not user_allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "data": None,
                    "error": {
                        "code": "RATE_LIMITED",
                        "msg": "Límite de requests por usuario excedido (1000 req/15min)",
                        "details": []
                    },
                    "meta": {
                        "timestamp": datetime.utcnow().isoformat(),
                        "rateLimit": user_info
                    }
                }
            )
    
    # Agregar headers de rate limit
    response.headers["X-RateLimit-Limit-IP"] = str(ip_info["limit"])
    response.headers["X-RateLimit-Remaining-IP"] = str(ip_info["remaining"])
    
    return response


# ============== MIDDLEWARE 3: JWT AUTHENTICATION ==============

security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """Extrae y valida JWT del header Authorization"""
    
    if not credentials:
        return None
    
    try:
        payload = verify_token(credentials.credentials)
        user = User(
            userId=payload.get("userId"),
            username=payload.get("username"),
            role=payload.get("role")
        )
        request.state.user = user.dict()
        return user
    except HTTPException:
        return None


def require_auth(user: Optional[User] = Depends(get_current_user)) -> User:
    """Dependencia que requiere autenticación"""
    if not user:
        raise HTTPException(
            status_code=401,
            detail="No autenticado"
        )
    return user


# ============== MIDDLEWARE 4: RBAC (Role-Based Access Control) ==============

def require_role(required_role: str):
    """Factory para crear dependencia de rol"""
    def role_checker(user: User = Depends(require_auth)) -> User:
        if user.role != required_role and required_role != UserRole.USER:
            # Admin puede acceder a rutas de user, pero no viceversa
            if not (user.role == UserRole.ADMIN and required_role == UserRole.USER):
                raise HTTPException(
                    status_code=403,
                    detail=f"Rol '{required_role}' requerido. Tu rol: '{user.role}'"
                )
        return user
    return role_checker


# ============== MIDDLEWARE 5: METRICS ==============

async def metrics_middleware(request: Request, call_next):
    """Captura métricas de latencia y status codes"""
    start_time = time.time()
    
    response = await call_next(request)
    
    latency = (time.time() - start_time) * 1000  # En ms
    endpoint = f"{request.method} {request.url.path}"
    
    # Registrar métrica
    metrics_storage[endpoint]["count"] += 1
    metrics_storage[endpoint]["latencies"].append(latency)
    
    if 400 <= response.status_code < 500:
        metrics_storage[endpoint]["status_4xx"] += 1
    elif response.status_code >= 500:
        metrics_storage[endpoint]["status_5xx"] += 1
    
    return response


# ============== MIDDLEWARE 6: STRUCTURED LOGGING ==============

async def logging_middleware(request: Request, call_next):
    """Logs estructurados en JSON"""
    start_time = time.time()
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    
    response = await call_next(request)
    
    latency = (time.time() - start_time) * 1000
    user_id = getattr(request.state, "user", {}).get("userId", None)
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": "INFO" if response.status_code < 400 else "ERROR",
        "correlationId": correlation_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "latency_ms": round(latency, 2),
        "userId": user_id,
        "client_ip": request.client.host
    }
    
    print(json.dumps(log_entry))  # En producción: usar logger estructurado
    
    return response


# ============== APLICACIÓN ==============

app = FastAPI(title="Secure API with JWT & Rate Limiting")

# Registrar middleware (orden IMPORTA - se ejecutan de arriba a abajo)
app.middleware("http")(correlation_id_middleware)
app.middleware("http")(rate_limiting_middleware)
app.middleware("http")(metrics_middleware)
app.middleware("http")(logging_middleware)


# ============== EXCEPTION HANDLERS ==============

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler para errores HTTP"""
    error_codes = {
        400: "BAD_REQUEST",
        401: "UNAUTHENTICATED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
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
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "correlationId": getattr(request.state, "correlation_id", None)
            }
        }
    )


# ============== RUTAS DE AUTENTICACIÓN ==============

@app.post("/api/v1/auth/login", response_model=dict)
async def login(request: Request, credentials: LoginRequest):
    """Login con username/password"""
    user_data = USERS_DB.get(credentials.username)
    
    if not user_data or user_data["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Crear tokens
    access_token = create_access_token({
        "userId": user_data["userId"],
        "username": user_data["username"],
        "role": user_data["role"]
    })
    
    refresh_token = create_refresh_token(user_data["userId"])
    
    response = JSONResponse(
        content={
            "data": {
                "accessToken": access_token,
                "expiresIn": ACCESS_TOKEN_EXPIRE_MINUTES * 60
            },
            "error": None,
            "meta": {
                "userId": user_data["userId"],
                "role": user_data["role"]
            }
        }
    )
    
    # Set refresh token en cookie HttpOnly
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        secure=False  # True en producción con HTTPS
    )
    
    return response


@app.post("/api/v1/auth/refresh")
async def refresh(request: Request):
    """Renovar access token con refresh token"""
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token or refresh_token not in refresh_tokens_db:
        raise HTTPException(status_code=401, detail="Refresh token inválido")
    
    token_data = refresh_tokens_db[refresh_token]
    
    # Verificar expiración
    if datetime.utcnow() > token_data["expiresAt"]:
        del refresh_tokens_db[refresh_token]
        raise HTTPException(status_code=401, detail="Refresh token expirado")
    
    # Obtener usuario
    user_id = token_data["userId"]
    user_data = next((u for u in USERS_DB.values() if u["userId"] == user_id), None)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    # Generar nuevo access token
    new_access_token = create_access_token({
        "userId": user_data["userId"],
        "username": user_data["username"],
        "role": user_data["role"]
    })
    
    return {
        "data": {
            "accessToken": new_access_token,
            "expiresIn": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        },
        "error": None,
        "meta": {}
    }


# ============== RUTAS PROTEGIDAS ==============

@app.get("/api/v1/user/profile")
async def get_profile(user: User = Depends(require_auth)):
    """Ruta protegida - requiere autenticación"""
    return {
        "data": user.dict(),
        "error": None,
        "meta": {}
    }


@app.get("/api/v1/admin/users")
async def list_users(user: User = Depends(require_role(UserRole.ADMIN))):
    """Ruta solo para admin"""
    return {
        "data": {
            "users": [
                {"userId": u["userId"], "username": u["username"], "role": u["role"]}
                for u in USERS_DB.values()
            ]
        },
        "error": None,
        "meta": {"requestedBy": user.username}
    }


@app.get("/api/v1/user/dashboard")
async def user_dashboard(user: User = Depends(require_role(UserRole.USER))):
    """Ruta para usuarios autenticados (user o admin)"""
    return {
        "data": {
            "message": f"Bienvenido al dashboard, {user.username}",
            "role": user.role
        },
        "error": None,
        "meta": {}
    }


# ============== MÉTRICAS ==============

@app.get("/api/v1/metrics")
async def get_metrics():
    """Endpoint de métricas (solo para demo)"""
    metrics_summary = {}
    
    for endpoint, data in metrics_storage.items():
        latencies = sorted(data["latencies"])
        n = len(latencies)
        
        metrics_summary[endpoint] = {
            "count": data["count"],
            "latency_p50": latencies[n // 2] if n > 0 else 0,
            "latency_p95": latencies[int(n * 0.95)] if n > 0 else 0,
            "status_4xx": data["status_4xx"],
            "status_5xx": data["status_5xx"],
            "error_rate": (data["status_4xx"] + data["status_5xx"]) / max(data["count"], 1) * 100
        }
    
    return {
        "data": metrics_summary,
        "error": None,
        "meta": {}
    }


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "service": "Secure API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
