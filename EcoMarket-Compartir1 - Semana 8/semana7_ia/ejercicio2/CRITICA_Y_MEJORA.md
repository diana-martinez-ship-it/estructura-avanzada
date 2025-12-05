# Crítica Técnica - Ejercicio 2: Middleware de Seguridad

---

## 📊 Evaluación de la Implementación Actual

### ✅ **FORTALEZAS**

#### 1. **Arquitectura de Middleware en Capas**
```
✅ Separación de concerns clara (6 capas independientes)
✅ Pipeline ordenado: correlationId → rateLimit → auth → rbac → metrics → logging
✅ Cada middleware tiene responsabilidad única
```

**Por qué es bueno:**
- Fácil añadir/remover capas sin afectar otras
- Testing aislado de cada capa
- Debugging simplificado (logs muestran qué capa falló)

---

#### 2. **Sistema de JWT Robusto**
```python
✅ Access tokens cortos (15 min) - reduce ventana de compromiso
✅ Refresh tokens largos (7 días) - mejora UX
✅ Refresh tokens en HttpOnly cookies - mitigación XSS
✅ Claims estructurados (userId, username, role, exp)
```

**Por qué es bueno:**
- Balance entre seguridad (tokens cortos) y experiencia (no re-login constante)
- Cookies HttpOnly no accesibles desde JavaScript → XSS no puede robar tokens
- Separación access/refresh permite revocar acceso sin afectar refresh

---

#### 3. **Rate Limiting Granular**
```
✅ Dos niveles: IP (100/15min) + userId (1000/15min)
✅ Sliding window algorithm - más justo que fixed window
✅ Headers RFC-compliant (X-RateLimit-*, Retry-After)
```

**Por qué es bueno:**
- IP limita DDoS/brute force
- userId limita abuso de cuentas comprometidas
- Sliding window evita "boundary gaming" (hacer 100 req a las 14:59:59)

---

#### 4. **RBAC Declarativo**
```python
@router.get("/admin/users", dependencies=[Depends(require_role("admin"))])
```

**Por qué es bueno:**
- Fácil leer permisos (se ven en la ruta)
- FastAPI valida antes de ejecutar handler
- Cambiar permisos no requiere modificar lógica de negocio

---

#### 5. **Observabilidad Integrada**
```json
{
  "correlationId": "uuid-123",
  "method": "GET",
  "path": "/user/profile",
  "statusCode": 200,
  "latencyMs": 45,
  "userId": "user1"
}
```

**Por qué es bueno:**
- Correlation ID permite tracing distribuido
- Logs estructurados (JSON) → fácil parseables por ELK/Splunk
- Métricas de latencia permiten detectar degradación

---

#### 6. **Manejo de Errores Estandarizado**
```json
{
  "data": null,
  "error": {"code": "UNAUTHENTICATED", "msg": "..."},
  "meta": {...}
}
```

**Por qué es bueno:**
- Cliente puede parsear errores consistentemente
- Códigos como `UNAUTHENTICATED`/`FORBIDDEN` son claros (no solo "error")
- `meta` provee contexto para debugging

---

### ❌ **DEBILIDADES**

#### 1. **Almacenamiento en Memoria**
```python
❌ rate_limit_storage = {}
❌ token_blacklist = set()
❌ mock_users_db = {...}
```

**Problema:**
- No persistente → restart pierde todo
- No funciona en múltiples instancias (cada proceso tiene su memoria)
- No hay límite → memory leak si crece indefinidamente

**Impacto:**
- ❌ No escalable horizontalmente
- ❌ Rate limit por IP se resetea en cada deploy
- ❌ Tokens revocados (blacklist) se pierden

**Solución:**
```python
# Usar Redis
import redis
r = redis.Redis(host='localhost', port=6379)

# Rate limit
key = f"ratelimit:{ip}:{window}"
r.incr(key)
r.expire(key, 900)  # TTL de 15 min

# Token blacklist
r.sadd("blacklist", token_jti)
r.expire(f"blacklist:{token_jti}", token_exp - now)
```

---

#### 2. **Falta Token Revocation**
```python
❌ No hay endpoint /logout
❌ No hay forma de invalidar tokens comprometidos
❌ Tokens siguen válidos hasta expirar (15 min)
```

**Problema:**
- Usuario hace logout → pero token sigue funcionando
- Cuenta comprometida → no puedes forzar cierre de sesión
- Cambio de rol → usuario mantiene rol viejo hasta que token expire

**Impacto:**
- ❌ Ventana de 15 min donde token robado funciona
- ❌ No hay forma de "emergency revoke" si detectas intrusión

**Solución:**
```python
@router.post("/logout")
async def logout(token_data: dict = Depends(get_current_user)):
    token_jti = token_data["jti"]  # Agregar JTI a claims
    redis.sadd("blacklist", token_jti)
    return {"msg": "Logged out"}

# En verify_token()
if redis.sismember("blacklist", token.get("jti")):
    raise HTTPException(401, detail="Token revoked")
```

---

#### 3. **Seguridad de Secreto JWT**
```python
❌ SECRET_KEY hardcodeado en código
❌ HS256 (simétrico) - mismo secreto para sign/verify
```

**Problema:**
- Secret en código → visible en git, leaks en logs
- HS256 requiere secret en cada servicio → mayor superficie de ataque
- Rotación de secret invalida TODOS los tokens

**Impacto:**
- ❌ Secret comprometido = cualquiera puede generar tokens válidos
- ❌ No puedes rotar secret sin romper todas las sesiones

**Solución:**
```python
# 1. Secret desde variables de entorno
import os
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY not set")

# 2. Usar RS256 (asimétrico)
from jwt.algorithms import RSAAlgorithm
with open("private_key.pem") as f:
    PRIVATE_KEY = RSAAlgorithm.from_jwk(f.read())
with open("public_key.pem") as f:
    PUBLIC_KEY = RSAAlgorithm.from_jwk(f.read())

# Sign con private, verify con public
jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
```

---

#### 4. **Rate Limiting Naive**
```python
❌ Limpieza de storage manual
❌ No hay priorización de requests
❌ IP puede ser spoofed/shared (NAT, proxies)
```

**Problema:**
- Storage crece sin límite (cada IP nueva añade entrada)
- Office con NAT → 100 empleados comparten 1 IP → bloqueados
- DDoS con IPs rotativas → storage explota

**Impacto:**
- ❌ Memory leak si hay muchas IPs
- ❌ Falsos positivos (usuarios legítimos bloqueados)

**Solución:**
```python
# 1. Token bucket con prioridad
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens/sec
    
    def consume(self, tokens=1, priority="normal"):
        if priority == "high":
            tokens *= 0.5  # High priority cuesta menos
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

# 2. Usar X-Forwarded-For + userId combinados
identifier = request.headers.get("X-Forwarded-For", ip)
if user_authenticated:
    identifier = f"user:{userId}"  # Priorizar userId sobre IP
```

---

#### 5. **Falta Auditoría**
```python
❌ No hay registro de eventos de seguridad
❌ No se loggean intentos de acceso no autorizado
❌ No hay alertas en patrones sospechosos
```

**Problema:**
- Ataque en curso → no te enteras hasta que es tarde
- Investigación post-mortem → no hay evidencia
- Compliance (GDPR, SOC2) → requiere audit trail

**Impacto:**
- ❌ No detectas brute force, credential stuffing
- ❌ No puedes rastrear quién accedió a qué

**Solución:**
```python
# Audit log estructurado
import logging
audit_logger = logging.getLogger("audit")

@router.post("/login")
async def login(credentials: LoginRequest):
    user = authenticate(credentials.username, credentials.password)
    
    if user:
        audit_logger.info({
            "event": "LOGIN_SUCCESS",
            "userId": user.id,
            "ip": request.client.host,
            "timestamp": datetime.utcnow()
        })
    else:
        audit_logger.warning({
            "event": "LOGIN_FAILED",
            "username": credentials.username,
            "ip": request.client.host,
            "timestamp": datetime.utcnow()
        })
        
        # Detectar patrón sospechoso
        failed_count = redis.incr(f"failed_login:{ip}")
        if failed_count > 5:
            alert_security_team(ip)
```

---

#### 6. **CORS Básico**
```python
❌ allow_origins=["*"] - permite cualquier origen
❌ No hay validación de Referer/Origin
```

**Problema:**
- Cualquier sitio puede hacer requests a tu API
- CSRF posible si usas cookies (como refresh_token)

**Impacto:**
- ❌ Sitio malicioso puede llamar API desde navegador del usuario

**Solución:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tuapp.com",
        "https://staging.tuapp.com"
    ],  # Solo tus dominios
    allow_credentials=True,  # Para cookies
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

# CSRF token para requests con cookies
from fastapi_csrf_protect import CsrfProtect

@router.post("/refresh")
async def refresh(csrf_token: str = Depends(CsrfProtect)):
    # Valida CSRF antes de refrescar
    ...
```

---

#### 7. **Métricas Incompletas**
```python
❌ Solo latencia y status codes
❌ No hay métricas de negocio (logins/min, tokens activos)
❌ No hay percentiles p99 (solo p50/p95)
```

**Problema:**
- No ves si hay spike de logins fallidos (posible ataque)
- No sabes cuántos usuarios activos hay
- p95 puede esconder outliers graves

**Solución:**
```python
from prometheus_client import Counter, Histogram, Gauge

login_attempts = Counter('login_attempts_total', 'Total login attempts', ['status'])
active_tokens = Gauge('active_tokens', 'Currently valid tokens')
request_latency = Histogram(
    'request_latency_seconds',
    'Request latency',
    buckets=[0.1, 0.25, 0.5, 1, 2.5, 5, 10]  # p99 detectable
)

@router.post("/login")
async def login(...):
    if success:
        login_attempts.labels(status='success').inc()
        active_tokens.inc()
    else:
        login_attempts.labels(status='failed').inc()
```

---

#### 8. **Testing Incompleto**
```python
❌ No hay tests de concurrencia
❌ No hay tests de tokens expirados
❌ No hay tests de rate limit por userId
```

**Problema:**
- Race conditions en rate limiting
- Edge case: token expira justo durante request
- No validas que userId rate limit funcione

**Solución:**
```python
import threading

def test_rate_limit_concurrent():
    """100 threads haciendo requests simultáneos"""
    def make_request():
        responses.append(client.get("/"))
    
    threads = [threading.Thread(target=make_request) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # Debe bloquear algunos
    assert sum(r.status_code == 429 for r in responses) > 0

def test_token_expires_during_request():
    """Token expira mientras se procesa request largo"""
    token = create_token(exp=time.time() + 1)  # Expira en 1 seg
    time.sleep(1.1)  # Esperar que expire
    
    response = client.get("/user/profile", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
```

---

## 🎯 **PROMPT MEJORADO**

```
Crea una API REST con FastAPI que implemente middleware de seguridad de grado producción:

REQUERIMIENTOS:

1. AUTENTICACIÓN JWT:
   - Access tokens RS256 (no HS256) con TTL 15 minutos
   - Refresh tokens en HttpOnly cookies (SameSite=Strict) con TTL 7 días
   - Agregar JTI (JWT ID) para revocación
   - Secreto desde variable de entorno JWT_SECRET_KEY
   - Endpoint POST /logout que blacklistea token

2. RATE LIMITING:
   - Usar Token Bucket Algorithm (no sliding window simple)
   - Tres niveles:
     * IP: 100 req/15min (anti-DDoS)
     * userId: 1000 req/15min (anti-abuso)
     * endpoint: /login 5 intentos/5min (anti-brute force)
   - Usar Redis para storage (redis-py)
   - Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After
   - Priorización: usuarios autenticados consumen 0.5x tokens

3. RBAC:
   - Roles: admin, user, guest
   - Permisos granulares: user:read, user:write, admin:*
   - Decorator @require_permission("user:write")
   - Chequeo de permisos antes de ejecutar handler

4. AUDITORÍA:
   - Logger separado para eventos de seguridad (audit.log)
   - Eventos: LOGIN_SUCCESS, LOGIN_FAILED, UNAUTHORIZED_ACCESS, TOKEN_REFRESHED, TOKEN_REVOKED
   - Formato JSON: {event, userId, ip, timestamp, userAgent, resource}
   - Alertar si >10 LOGIN_FAILED desde misma IP en 5 min

5. CORS & CSRF:
   - CORS: allow_origins desde env var (no wildcard)
   - CSRF protection en endpoints con cookies (fastapi-csrf-protect)
   - Validar Referer header en requests sensibles

6. MÉTRICAS PROMETHEUS:
   - Counter: login_attempts_total{status="success|failed"}
   - Gauge: active_tokens, active_sessions
   - Histogram: request_latency_seconds (buckets: 0.1, 0.5, 1, 5)
   - Endpoint GET /metrics en formato Prometheus

7. TESTING:
   - 15 tests pytest:
     * Auth: login exitoso, credenciales inválidas, token expirado, token revocado
     * Rate limit: dentro de límite, excede límite IP, excede límite user, concurrencia
     * RBAC: admin accede recurso admin, user bloqueado de recurso admin
     * CSRF: request con/sin token CSRF
     * Métricas: verificar incremento de counters
   - Fixtures para Redis test (redis-py test utilities)

8. MANEJO DE ERRORES:
   - Respuestas estandarizadas: {data, error: {code, msg, details}, meta}
   - Códigos: UNAUTHENTICATED, FORBIDDEN, RATE_LIMITED, INVALID_CREDENTIALS, TOKEN_EXPIRED
   - Exception handlers para 401, 403, 429, 500
   - Logging de errores con stack traces

9. CONFIGURACIÓN:
   - Usar pydantic-settings para config desde env:
     * JWT_SECRET_KEY (required)
     * REDIS_URL (default: redis://localhost:6379)
     * ALLOWED_ORIGINS (default: [])
     * RATE_LIMIT_IP (default: 100)
   - Validar que secrets estén seteadas al startup

10. DEPENDENCIAS:
    fastapi==0.104.0
    pyjwt[crypto]==2.8.0  # Para RS256
    redis==5.0.0
    prometheus-client==0.19.0
    fastapi-csrf-protect==0.3.0
    pydantic-settings==2.0.0
    pytest==7.4.0
    httpx==0.25.0

ENTREGABLES:
- api_secure_v2.py (código completo con todos los middlewares)
- test_security_v2.py (15 tests)
- config.py (configuración con pydantic-settings)
- requirements.txt
- README.md con instrucciones de deploy (Redis, env vars)
- SECURITY.md documentando threat model y mitigaciones

CRITERIOS DE ÉXITO:
✅ Tokens JWT con RS256 y revocación funcionando
✅ Rate limiting multinivel con Redis
✅ Audit log capturando eventos de seguridad
✅ 15/15 tests pasando
✅ Métricas Prometheus accesibles en /metrics
✅ CSRF protection en endpoints con cookies
✅ Config desde env vars (no hardcoded)
```

---

## 📈 **COMPARACIÓN: ANTES vs DESPUÉS**

| Aspecto | Implementación Actual | Propuesta Mejorada |
|---------|----------------------|-------------------|
| **Algoritmo JWT** | HS256 (simétrico) | RS256 (asimétrico) |
| **Secreto** | Hardcoded | Variable de entorno |
| **Revocación** | ❌ No soportada | ✅ Blacklist con JTI |
| **Storage** | Memoria (dict) | Redis persistente |
| **Rate Limit** | Sliding window | Token bucket + priorización |
| **Auditoría** | ❌ No implementada | ✅ Audit log + alertas |
| **CORS** | allow_origins=["*"] | Dominios específicos desde env |
| **CSRF** | ❌ No protegido | ✅ CSRF tokens |
| **Métricas** | Latency + status | + Prometheus counters/gauges |
| **Tests** | 6 tests básicos | 15 tests + concurrencia |
| **Config** | Hardcoded | pydantic-settings + validación |
| **Escalabilidad** | ❌ Single instance | ✅ Horizontal (Redis compartido) |

---

## 🔐 **THREAT MODEL**

### Amenazas Mitigadas:
✅ **XSS** → Tokens en HttpOnly cookies  
✅ **CSRF** → CSRF tokens en cookies  
✅ **DDoS** → Rate limiting por IP  
✅ **Brute Force** → Rate limiting en /login  
✅ **Token Hijacking** → Tokens cortos + revocación  
✅ **Privilege Escalation** → RBAC estricto

### Amenazas Residuales:
⚠️ **Compromiso de Private Key** → Necesita HSM en producción  
⚠️ **Redis SPOF** → Necesita Redis Cluster con replicas  
⚠️ **Timing Attacks** → Agregar delays aleatorios en auth  

---

## 💡 **CONCLUSIÓN**

**Implementación actual: 7/10**
- ✅ Excelente punto de partida para prototipo
- ✅ Arquitectura limpia y extensible
- ❌ No production-ready (storage en memoria fatal)

**Con mejoras propuestas: 9.5/10**
- ✅ Escalable horizontalmente
- ✅ Auditable y observable
- ✅ Seguro contra ataques comunes
- ⚠️ Falta HSM para private keys (enterprise)
