"""
DIAGRAMA DEL PIPELINE DE MIDDLEWARE - Ejercicio 2
"""

PIPELINE_ASCII = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                    REQUEST PIPELINE - MIDDLEWARE STACK                     ║
╚═══════════════════════════════════════════════════════════════════════════╝

    Cliente HTTP Request
         │
         ├──────────────────────────────────────────────────────┐
         │                                                       │
         ▼                                                       │
    ┌─────────────────────────────────────────┐                │
    │  1️⃣  CORRELATION ID MIDDLEWARE          │                │
    │  • Genera UUID único por request        │                │
    │  • Agrega X-Correlation-ID a headers    │                │
    │  • Inyecta correlation_id en logs       │                │
    └──────────────┬──────────────────────────┘                │
                   │                                            │
                   ▼                                            │
    ┌─────────────────────────────────────────┐                │
    │  2️⃣  RATE LIMITING MIDDLEWARE           │                │
    │  • Extrae IP y userId (si autenticado)  │                │
    │  • Verifica límites:                    │                │
    │    - 100 req/15min por IP               │ ──────────────┼─→ 429 Too Many Requests
    │    - 1000 req/15min por userId          │                │   { error: "RATE_LIMITED" }
    │  • Usa memoria/Redis para contadores    │                │
    └──────────────┬──────────────────────────┘                │
                   │                                            │
                   ▼                                            │
    ┌─────────────────────────────────────────┐                │
    │  3️⃣  JWT AUTHENTICATION MIDDLEWARE      │                │
    │  • Extrae Bearer token de Authorization │                │
    │  • Valida JWT (firma, expiración)       │ ──────────────┼─→ 401 Unauthorized
    │  • Decodifica payload (userId, role)    │                │   { error: "UNAUTHENTICATED" }
    │  • Valida refresh token de cookie       │                │
    │  • Inyecta usuario en request.state     │                │
    └──────────────┬──────────────────────────┘                │
                   │                                            │
                   ▼                                            │
    ┌─────────────────────────────────────────┐                │
    │  4️⃣  ROLE-BASED ACCESS CONTROL (RBAC)  │                │
    │  • Verifica role del usuario            │                │
    │  • Valida permisos por ruta:            │ ──────────────┼─→ 403 Forbidden
    │    - /api/v1/admin/* → solo "admin"     │                │   { error: "FORBIDDEN" }
    │    - /api/v1/user/* → "admin" o "user"  │                │
    └──────────────┬──────────────────────────┘                │
                   │                                            │
                   ▼                                            │
    ┌─────────────────────────────────────────┐                │
    │  5️⃣  METRICS COLLECTION MIDDLEWARE      │                │
    │  • Captura timestamp de inicio          │                │
    │  • Ejecuta endpoint                     │ ───────────────┘
    │  • Mide latencia (end - start)          │
    │  • Registra métricas:                   │
    │    - Latencia p50/p95                   │
    │    - Status codes 4xx/5xx               │
    │    - Contadores por endpoint            │
    └──────────────┬──────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────────┐
    │  6️⃣  STRUCTURED LOGGING                 │
    │  • Log JSON con:                        │
    │    - timestamp                          │
    │    - level (INFO/WARN/ERROR)            │
    │    - correlationId                      │
    │    - method, path                       │
    │    - status_code                        │
    │    - latency_ms                         │
    │    - userId (si existe)                 │
    │    - error_details (si hay)             │
    └──────────────┬──────────────────────────┘
                   │
                   ▼
         HTTP Response al Cliente
         (con headers: X-Correlation-ID, X-RateLimit-*)


╔═══════════════════════════════════════════════════════════════════════════╗
║                         JWT TOKEN FLOW (Detalle)                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

    LOGIN /api/v1/auth/login
         │
         ├─ Valida credenciales (user/pass)
         │
         ├─ Genera Access Token JWT (HS256)
         │  • Payload: { userId, role, exp: 15min }
         │  • Header: Authorization: Bearer <access_token>
         │
         ├─ Genera Refresh Token (UUID)
         │  • Almacena en DB/Redis con TTL 7 días
         │  • Cookie: Set-Cookie: refresh_token=<uuid>; 
         │           HttpOnly; SameSite=Lax; Max-Age=604800
         │
         └─ Response:
            {
              "data": {
                "accessToken": "<jwt>",
                "expiresIn": 900
              },
              "meta": { "userId": "123" }
            }


    REFRESH /api/v1/auth/refresh
         │
         ├─ Lee refresh_token de cookie
         │
         ├─ Valida en DB/Redis
         │
         ├─ Genera nuevo Access Token
         │
         └─ Response: { "accessToken": "<new_jwt>" }


    PROTECTED REQUEST /api/v1/products
         │
         ├─ Header: Authorization: Bearer <access_token>
         │
         ├─ Middleware valida JWT
         │  • jwt.decode(token, SECRET, algorithms=["HS256"])
         │  • Verifica exp, iss, sub
         │
         ├─ Extrae userId y role
         │
         ├─ Inyecta en request.state.user = { userId, role }
         │
         └─ Endpoint ejecuta con contexto de usuario


╔═══════════════════════════════════════════════════════════════════════════╗
║                      RATE LIMITING ALGORITHM                              ║
╚═══════════════════════════════════════════════════════════════════════════╝

    Sliding Window Counter (por IP y userId)

    ┌────────────────────────────────────────────────────┐
    │  Ventana: 15 minutos = 900 segundos                │
    │  Límite: 100 req/15min (IP) | 1000 req/15min (user)│
    └────────────────────────────────────────────────────┘

    Timestamp actual: 1700000000

    Requests en ventana:
    ┌─────────────────────────────────────────┐
    │  1699999100  1699999200  1699999500  ... │  ← Timestamps
    │      ▓           ▓           ▓          │  ← Requests
    │  |─────────────── 900s ───────────────| │  ← Window
    └─────────────────────────────────────────┘
                      current_time

    Algoritmo:
    1. current_time = time.time()
    2. window_start = current_time - 900
    3. count = len([r for r in requests if r > window_start])
    4. if count >= limit:
           return 429 Too Many Requests
    5. else:
           requests.append(current_time)
           return OK


    Headers en respuesta:
    ┌──────────────────────────────────────────┐
    │  X-RateLimit-Limit: 100                  │
    │  X-RateLimit-Remaining: 42               │
    │  X-RateLimit-Reset: 1700000900           │
    │  Retry-After: 300                        │  (si 429)
    └──────────────────────────────────────────┘
"""

print(PIPELINE_ASCII)
