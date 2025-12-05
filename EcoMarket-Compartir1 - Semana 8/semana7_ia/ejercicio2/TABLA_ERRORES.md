# TABLA DE RESPUESTAS DE ERROR - Ejercicio 2

## 📊 Respuestas Estandarizadas

### 🔴 401 UNAUTHORIZED (No autenticado)

**Casos:**
- Sin header Authorization
- Token JWT inválido o mal formado
- Token JWT expirado
- Refresh token inválido

**Respuesta HTTP 401:**
```json
{
  "data": null,
  "error": {
    "code": "UNAUTHENTICATED",
    "msg": "Token expirado",
    "details": []
  },
  "meta": {
    "timestamp": "2025-11-26T12:00:00Z",
    "correlationId": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Headers:**
```
WWW-Authenticate: Bearer realm="api"
X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440000
```

---

### 🔴 403 FORBIDDEN (Sin permisos)

**Casos:**
- Usuario autenticado pero sin rol adecuado
- Usuario "user" intenta acceder a ruta /api/v1/admin/*
- Token válido pero permisos insuficientes

**Respuesta HTTP 403:**
```json
{
  "data": null,
  "error": {
    "code": "FORBIDDEN",
    "msg": "Rol 'admin' requerido. Tu rol: 'user'",
    "details": []
  },
  "meta": {
    "timestamp": "2025-11-26T12:00:00Z",
    "correlationId": "550e8400-e29b-41d4-a716-446655440001"
  }
}
```

**Headers:**
```
X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440001
```

---

### 🔴 429 TOO MANY REQUESTS (Rate limit excedido)

**Casos:**
- Más de 100 requests en 15 minutos desde la misma IP
- Más de 1000 requests en 15 minutos por el mismo userId

**Respuesta HTTP 429:**

#### Por IP:
```json
{
  "data": null,
  "error": {
    "code": "RATE_LIMITED",
    "msg": "Límite de requests por IP excedido (100 req/15min)",
    "details": []
  },
  "meta": {
    "timestamp": "2025-11-26T12:00:00Z",
    "rateLimit": {
      "limit": 100,
      "remaining": 0,
      "reset": 1700001000
    }
  }
}
```

#### Por userId:
```json
{
  "data": null,
  "error": {
    "code": "RATE_LIMITED",
    "msg": "Límite de requests por usuario excedido (1000 req/15min)",
    "details": []
  },
  "meta": {
    "timestamp": "2025-11-26T12:00:00Z",
    "rateLimit": {
      "limit": 1000,
      "remaining": 0,
      "reset": 1700001900
    }
  }
}
```

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1700001000
Retry-After: 300
X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440002
```

---

## 📋 TABLA COMPARATIVA

| Status | Code | Mensaje | Cuándo Ocurre | Retry? | Headers Especiales |
|--------|------|---------|---------------|--------|-------------------|
| **401** | `UNAUTHENTICATED` | Token expirado / inválido | Sin auth o token malo | ✅ Sí (con nuevo token) | `WWW-Authenticate` |
| **403** | `FORBIDDEN` | Rol insuficiente | Token válido pero sin permisos | ❌ No (cambiar permisos) | - |
| **429** | `RATE_LIMITED` | Límite excedido | Demasiados requests | ✅ Sí (después de reset) | `X-RateLimit-*`, `Retry-After` |

---

## 🔍 DETALLES POR ERROR

### 401 UNAUTHENTICATED - Variantes

| Variante | Mensaje | Causa |
|----------|---------|-------|
| Sin token | "No autenticado" | Header Authorization vacío |
| Token expirado | "Token expirado" | JWT `exp` < now |
| Token inválido | "Token inválido" | Firma no válida o payload corrupto |
| Refresh inválido | "Refresh token inválido" | Cookie no existe en DB |
| Refresh expirado | "Refresh token expirado" | TTL de 7 días pasó |

### 403 FORBIDDEN - Variantes

| Variante | Mensaje | Causa |
|----------|---------|-------|
| Rol insuficiente | "Rol 'admin' requerido. Tu rol: 'user'" | Usuario sin permisos |
| Recurso prohibido | "Acceso denegado a este recurso" | Política personalizada |

### 429 RATE_LIMITED - Variantes

| Variante | Mensaje | Límite | Window |
|----------|---------|--------|--------|
| Por IP | "Límite de requests por IP excedido" | 100 req | 15 min |
| Por userId | "Límite de requests por usuario excedido" | 1000 req | 15 min |

---

## 🎯 FLUJO DE MANEJO DE ERRORES

```
Cliente hace request
    │
    ├─ Middleware 1: Correlation ID  ────────────────┐
    │                                                 │
    ├─ Middleware 2: Rate Limiting                   │
    │      └─ ❌ Excedido → 429 + headers ───────────┤
    │                                                 │
    ├─ Middleware 3: JWT Auth                        │
    │      └─ ❌ Token inválido → 401 ───────────────┤
    │                                                 │
    ├─ Middleware 4: RBAC                            │
    │      └─ ❌ Sin permisos → 403 ─────────────────┤
    │                                                 │
    ├─ Endpoint ejecuta ✅                           │
    │                                                 │
    └─ Exception Handler ─────────────────────────────┘
           │
           └─ Formatea respuesta JSON estándar
              con código, mensaje, detalles y meta
```

---

## 📝 EJEMPLOS DE USO

### Ejemplo 1: Token expirado
```bash
curl -H "Authorization: Bearer <expired_token>" \
     http://localhost:8000/api/v1/user/profile
```

**Respuesta:**
```json
{
  "data": null,
  "error": {
    "code": "UNAUTHENTICATED",
    "msg": "Token expirado",
    "details": []
  },
  "meta": {
    "timestamp": "2025-11-26T12:00:00Z",
    "correlationId": "abc-123"
  }
}
```

**Solución:** Renovar token con `/api/v1/auth/refresh`

---

### Ejemplo 2: Usuario sin rol admin
```bash
# Login como "user1"
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"user123"}' \
  | jq -r '.data.accessToken')

# Intentar acceder a ruta de admin
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/v1/admin/users
```

**Respuesta:**
```json
{
  "data": null,
  "error": {
    "code": "FORBIDDEN",
    "msg": "Rol 'admin' requerido. Tu rol: 'user'",
    "details": []
  },
  "meta": {
    "timestamp": "2025-11-26T12:00:00Z",
    "correlationId": "def-456"
  }
}
```

**Solución:** Usar cuenta con rol admin

---

### Ejemplo 3: Rate limit excedido
```bash
# Hacer 101 requests seguidos
for i in {1..101}; do
  curl http://localhost:8000/
done
```

**Respuesta (request #101):**
```json
{
  "data": null,
  "error": {
    "code": "RATE_LIMITED",
    "msg": "Límite de requests por IP excedido (100 req/15min)",
    "details": []
  },
  "meta": {
    "timestamp": "2025-11-26T12:00:00Z",
    "rateLimit": {
      "limit": 100,
      "remaining": 0,
      "reset": 1700001900
    }
  }
}
```

**Headers:**
```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1700001900
Retry-After: 300
```

**Solución:** Esperar 300 segundos (5 min) o hasta `reset` timestamp

---

## 🔒 MEJORES PRÁCTICAS

### Para clientes API:

1. **401 - Renovar token automáticamente:**
   ```javascript
   if (response.status === 401) {
     const newToken = await refreshToken();
     return retryRequest(newToken);
   }
   ```

2. **403 - No reintentar, mostrar error:**
   ```javascript
   if (response.status === 403) {
     showError("No tienes permisos para esta acción");
   }
   ```

3. **429 - Esperar y reintentar:**
   ```javascript
   if (response.status === 429) {
     const retryAfter = response.headers['Retry-After'];
     await sleep(retryAfter * 1000);
     return retryRequest();
   }
   ```

### Para el servidor:

1. **Siempre incluir `correlationId`** para trazabilidad
2. **Usar headers estándar** (`WWW-Authenticate`, `Retry-After`)
3. **Mensajes descriptivos** sin revelar detalles de seguridad
4. **Logs estructurados** de cada error para debugging
