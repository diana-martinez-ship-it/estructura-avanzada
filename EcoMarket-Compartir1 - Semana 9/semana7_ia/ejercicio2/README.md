# 🔐 Ejercicio 2: Middleware de Autenticación y Rate Limiting

Sistema completo de seguridad con JWT, rate limiting, RBAC y observabilidad.

---

## 📋 Contenido

```
ejercicio2/
├── api_secure.py            # API con 6 capas de middleware
├── test_security.py         # 6 tests (3 exitosos + 3 fallidos)
├── diagrama_pipeline.py     # Diagramas ASCII del pipeline
├── TABLA_ERRORES.md         # Documentación de errores (401, 403, 429)
├── CRITICA_Y_MEJORA.md      # Análisis técnico + prompt mejorado
└── README.md                # Este archivo
```

---

## 🚀 Quickstart

### 1. Instalar Dependencias

```powershell
pip install fastapi==0.104.0 uvicorn pyjwt python-multipart httpx
```

### 2. Ejecutar API

```powershell
cd semana7_ia\ejercicio2
uvicorn api_secure:app --reload --port 8000
```

Verás:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 3. Probar con curl

#### ✅ Login Exitoso
```powershell
curl -X POST http://localhost:8000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{"username": "admin", "password": "admin123"}' `
  -c cookies.txt

# Respuesta:
# {
#   "data": {
#     "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#     "expiresIn": 900
#   },
#   "error": null
# }
```

#### ✅ Acceder a Ruta Protegida
```powershell
$TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # Token del paso anterior

curl http://localhost:8000/api/v1/user/profile `
  -H "Authorization: Bearer $TOKEN"

# Respuesta:
# {
#   "data": {
#     "userId": "admin",
#     "username": "admin",
#     "role": "admin"
#   },
#   "error": null
# }
```

#### ❌ Error 401: Sin Token
```powershell
curl http://localhost:8000/api/v1/user/profile

# Respuesta:
# {
#   "data": null,
#   "error": {
#     "code": "UNAUTHENTICATED",
#     "msg": "No autenticado. Token requerido."
#   }
# }
```

---

## 🧪 Ejecutar Tests

```powershell
# Método 1: Con pytest
pip install pytest
pytest test_security.py -v

# Método 2: Directamente con Python
python test_security.py
```

**Salida esperada:**
```
======================================================================
  SUITE DE PRUEBAS - EJERCICIO 2
  Autenticación JWT + Rate Limiting + RBAC
======================================================================

🟢 ====================================================================
  PRUEBAS EXITOSAS (3)
======================================================================

TEST 1: ✅ Login exitoso
✅ Token JWT generado correctamente
✅ Access Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
✅ Cookie refresh_token configurada

TEST 2: ✅ Acceso a ruta protegida con autenticación
✅ Usuario autenticado correctamente
✅ Correlation ID: 123e4567-e89b-12d3-a456-426614174000
✅ Rate Limit IP: 99/100

TEST 3: ✅ Admin accede a ruta restringida
✅ Admin accedió exitosamente
✅ Usuarios listados: 2

🔴 ====================================================================
  PRUEBAS FALLIDAS (3)
======================================================================

TEST 4: ❌ Acceso sin autenticación
❌ Código de error: UNAUTHENTICATED

TEST 5: ❌ Usuario sin permisos intenta ruta admin
❌ Código de error: FORBIDDEN

TEST 6: ❌ Rate limit excedido
❌ Límite: 100
❌ Restantes: 0
❌ Retry-After: 900s

  ✅ RESUMEN: 6/6 pruebas ejecutadas correctamente
```

---

## 🏗️ Arquitectura

### Pipeline de Middleware (6 Capas)

```
Request
   ↓
[1] CorrelationIDMiddleware  ← Genera UUID para tracing
   ↓
[2] RateLimitingMiddleware   ← Verifica límites (IP + userId)
   ↓
[3] JWTAuthMiddleware        ← Valida token Bearer
   ↓
[4] RBACMiddleware           ← Chequea permisos de rol
   ↓
[5] MetricsMiddleware        ← Registra latencia
   ↓
[6] StructuredLogMiddleware  ← Log JSON estructurado
   ↓
Handler (endpoint)
```

### Flujo de JWT

```
┌─────────┐                    ┌─────────┐
│ Cliente │                    │   API   │
└────┬────┘                    └────┬────┘
     │                              │
     │  POST /login                 │
     │  {username, password}        │
     ├─────────────────────────────>│
     │                              │
     │                              │ ✅ Validar credenciales
     │                              │ ✅ Generar accessToken (15 min)
     │                              │ ✅ Generar refreshToken (7 días)
     │                              │
     │  200 OK                      │
     │  {accessToken: "..."}        │
     │  Set-Cookie: refresh_token   │
     │<─────────────────────────────┤
     │                              │
     │  GET /user/profile           │
     │  Authorization: Bearer ...   │
     ├─────────────────────────────>│
     │                              │
     │                              │ ✅ Verificar firma JWT
     │                              │ ✅ Verificar expiración
     │                              │ ✅ Extraer userId/role
     │                              │
     │  200 OK                      │
     │  {userId, username, role}    │
     │<─────────────────────────────┤
```

---

## 📊 Rate Limiting

### Límites Configurados

| Tipo | Límite | Ventana | Identificador |
|------|--------|---------|---------------|
| **IP** | 100 req | 15 min | `request.client.host` |
| **Usuario** | 1000 req | 15 min | `token.userId` |

### Algoritmo: Sliding Window

```
Ventana de 15 minutos:

Timestamps guardados: [t1, t2, t3, ...]
                       ↓
Filtrar últimos 15 min: [t_now-900, t_now]
                       ↓
Contar requests: len(filtrado)
                       ↓
Si count < límite → ✅ Permitir
Si count >= límite → ❌ Bloquear (429)
```

### Headers de Rate Limit

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit-IP: 100
X-RateLimit-Remaining-IP: 0
X-RateLimit-Reset-IP: 1735689600
Retry-After: 873
```

---

## 🔑 Autenticación

### Credenciales de Prueba

| Usuario | Password | Rol |
|---------|----------|-----|
| `admin` | `admin123` | `admin` |
| `user1` | `user123` | `user` |

### Token JWT (Claims)

```json
{
  "userId": "admin",
  "username": "admin",
  "role": "admin",
  "exp": 1735689600,
  "iat": 1735688700
}
```

**Configuración:**
- **Algoritmo:** HS256
- **Secret:** `mi-secreto-super-seguro-cambiar-en-produccion`
- **Access Token TTL:** 15 minutos (900 segundos)
- **Refresh Token TTL:** 7 días (604800 segundos)

### Refresh Token (Cookie)

```http
Set-Cookie: refresh_token=eyJhbGciOiJIUzI1NiI...;
            HttpOnly;
            SameSite=Lax;
            Max-Age=604800
```

**Propiedades:**
- `HttpOnly` → JavaScript no puede leer (mitigación XSS)
- `SameSite=Lax` → Protección básica CSRF
- `Max-Age` → Expira en 7 días

---

## 🛡️ RBAC (Control de Acceso Basado en Roles)

### Matriz de Permisos

| Endpoint | Método | Admin | User | Guest |
|----------|--------|-------|------|-------|
| `/` | GET | ✅ | ✅ | ✅ |
| `/api/v1/auth/login` | POST | ✅ | ✅ | ✅ |
| `/api/v1/auth/refresh` | POST | ✅ | ✅ | ✅ |
| `/api/v1/user/profile` | GET | ✅ | ✅ | ❌ |
| `/api/v1/user/dashboard` | GET | ✅ | ✅ | ❌ |
| `/api/v1/admin/users` | GET | ✅ | ❌ | ❌ |

### Ejemplo de Restricción

```python
@router.get("/admin/users", dependencies=[Depends(require_role("admin"))])
async def get_users():
    ...
```

Si un usuario con rol `user` intenta acceder:
```json
{
  "data": null,
  "error": {
    "code": "FORBIDDEN",
    "msg": "Requiere rol: admin"
  }
}
```

---

## 📈 Métricas y Observabilidad

### Endpoint de Métricas

```powershell
curl http://localhost:8000/api/v1/metrics
```

**Respuesta:**
```json
{
  "requests": {
    "total": 1523,
    "by_status": {
      "200": 1234,
      "401": 156,
      "403": 89,
      "429": 44
    }
  },
  "latency": {
    "p50": 23.5,
    "p95": 87.2,
    "p99": 156.8
  },
  "rate_limit": {
    "blocked_ips": 12,
    "blocked_users": 3
  }
}
```

### Logs Estructurados

```json
{
  "timestamp": "2025-01-31T12:34:56.789Z",
  "correlationId": "123e4567-e89b-12d3-a456-426614174000",
  "level": "INFO",
  "method": "GET",
  "path": "/api/v1/user/profile",
  "statusCode": 200,
  "latencyMs": 23.5,
  "userId": "user1",
  "ip": "127.0.0.1"
}
```

**Campos clave:**
- `correlationId` → Tracing distribuido (vincular logs de múltiples servicios)
- `latencyMs` → Detectar degradación de performance
- `userId` → Auditoría (quién hizo qué)

---

## ❌ Manejo de Errores

Ver documentación completa en **[TABLA_ERRORES.md](TABLA_ERRORES.md)**

### Códigos de Error

| Código HTTP | Error Code | Descripción |
|-------------|-----------|-------------|
| `401` | `UNAUTHENTICATED` | Token ausente, inválido o expirado |
| `403` | `FORBIDDEN` | Usuario no tiene permisos para el recurso |
| `429` | `RATE_LIMITED` | Límite de requests excedido (IP o userId) |

### Formato de Respuesta de Error

```json
{
  "data": null,
  "error": {
    "code": "UNAUTHENTICATED",
    "msg": "Token expirado. Usa /refresh para obtener uno nuevo."
  },
  "meta": {
    "timestamp": "2025-01-31T12:34:56Z",
    "correlationId": "abc-123"
  }
}
```

---

## 🔧 Configuración

### Variables de Entorno (Producción)

```bash
# JWT
JWT_SECRET_KEY=mi-secreto-super-seguro-cambiar-en-produccion
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Rate Limiting
RATE_LIMIT_IP=100
RATE_LIMIT_USER=1000
RATE_LIMIT_WINDOW_SECONDS=900

# CORS
ALLOWED_ORIGINS=https://miapp.com,https://staging.miapp.com

# Redis (para producción)
REDIS_URL=redis://localhost:6379/0
```

### Ejemplo con Docker

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

---

## 🧩 Extensiones Futuras

### 1. Token Revocation
```python
@router.post("/logout")
async def logout(token: dict = Depends(get_current_user)):
    # Agregar token a blacklist (Redis)
    redis.sadd("blacklist", token["jti"])
    return {"msg": "Logged out"}
```

### 2. RS256 (Asimétrico)
```python
# Generar par de llaves
# openssl genrsa -out private.pem 2048
# openssl rsa -in private.pem -pubout -out public.pem

from jwt.algorithms import RSAAlgorithm
with open("private.pem") as f:
    PRIVATE_KEY = RSAAlgorithm.from_jwk(f.read())

jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
```

### 3. Audit Log
```python
audit_logger = logging.getLogger("audit")

audit_logger.info({
    "event": "LOGIN_SUCCESS",
    "userId": user.id,
    "ip": request.client.host,
    "timestamp": datetime.utcnow()
})
```

---

## 📚 Documentación Relacionada

- **[diagrama_pipeline.py](diagrama_pipeline.py)** - Diagramas ASCII del pipeline de middleware
- **[TABLA_ERRORES.md](TABLA_ERRORES.md)** - Catálogo completo de errores con ejemplos
- **[CRITICA_Y_MEJORA.md](CRITICA_Y_MEJORA.md)** - Análisis técnico y prompt mejorado
- **[test_security.py](test_security.py)** - Suite de tests con casos de éxito y fallo

---

## 🎯 Criterios de Evaluación

| Criterio | Estado | Evidencia |
|----------|--------|-----------|
| ✅ JWT con access + refresh tokens | Implementado | `api_secure.py` L50-90 |
| ✅ Rate limiting (IP + userId) | Implementado | `api_secure.py` L100-150 |
| ✅ RBAC con roles admin/user | Implementado | `api_secure.py` L200-240 |
| ✅ Middleware en pipeline ordenado | Implementado | 6 capas secuenciales |
| ✅ Logs estructurados JSON | Implementado | `api_secure.py` L300-350 |
| ✅ Métricas de latencia (p50/p95) | Implementado | `api_secure.py` L400-450 |
| ✅ Manejo de errores estandarizado | Implementado | `TABLA_ERRORES.md` |
| ✅ 3 tests exitosos + 3 fallidos | Implementado | `test_security.py` |
| ✅ Diagrama del pipeline | Implementado | `diagrama_pipeline.py` |
| ✅ Crítica técnica | Implementado | `CRITICA_Y_MEJORA.md` |

---

## 🚨 Notas de Seguridad

### ⚠️ Solo para Desarrollo

Esta implementación usa:
- **Almacenamiento en memoria** (no persistente)
- **Secret hardcoded** (cambiar en producción)
- **CORS permisivo** (configurar dominios reales)

### ✅ Producción Requiere

1. **Redis** para storage compartido (rate limiting, blacklist)
2. **Secrets en variables de entorno** (no en código)
3. **HTTPS** obligatorio (para cookies seguras)
4. **Monitoring** (Prometheus, Grafana)
5. **WAF** (Web Application Firewall) para ataques layer 7

---

## 📖 Referencias

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OWASP Rate Limiting](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html)
- [RBAC Explained](https://en.wikipedia.org/wiki/Role-based_access_control)

---

**Autor:** Ejercicio 2 - Semana 7 IA  
**Fecha:** Enero 2025  
**Versión:** 1.0
