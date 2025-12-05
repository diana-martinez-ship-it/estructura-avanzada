# Ejemplos de Logs Estructurados - Ejercicio 5

Este archivo muestra ejemplos reales de logs JSON estructurados generados por `api_observable.py`.

---

## 📝 LOG 1: Request Exitosa (CREATE Product)

```json
{
  "ts": "2025-11-26T13:42:15.123456Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Request started",
  "correlationId": "550e8400-e29b-41d4-a716-446655440000",
  "method": "POST",
  "path": "/api/v1/products",
  "userId": "user123"
}
```

```json
{
  "ts": "2025-11-26T13:42:15.135678Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Trace step: validating_input",
  "correlationId": "550e8400-e29b-41d4-a716-446655440000",
  "step": "validating_input",
  "elapsed_ms": 3.45
}
```

```json
{
  "ts": "2025-11-26T13:42:15.143210Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Product created",
  "correlationId": "550e8400-e29b-41d4-a716-446655440000",
  "product_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "iPhone 15 Pro"
}
```

```json
{
  "ts": "2025-11-26T13:42:15.147890Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Request completed",
  "correlationId": "550e8400-e29b-41d4-a716-446655440000",
  "method": "POST",
  "path": "/api/v1/products",
  "status": 201,
  "latency_ms": 12.34,
  "userId": "user123"
}
```

**Análisis:**
- ✅ correlationId único para trazar toda la request
- ✅ Timestamps precisos (microsegundos)
- ✅ Latency medida: 12.34ms (bajo umbral de 50ms)
- ✅ userId presente para auditoría
- ✅ Status 201 = Created (exitoso)

---

## ❌ LOG 2: Error 404 (Product Not Found)

```json
{
  "ts": "2025-11-26T13:45:22.456789Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Request started",
  "correlationId": "abc123-def456-ghi789",
  "method": "GET",
  "path": "/api/v1/products/00000000-0000-0000-0000-000000000000",
  "userId": "user456"
}
```

```json
{
  "ts": "2025-11-26T13:45:22.461234Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Trace step: querying_database",
  "correlationId": "abc123-def456-ghi789",
  "step": "querying_database",
  "elapsed_ms": 2.1
}
```

```json
{
  "ts": "2025-11-26T13:45:22.463456Z",
  "level": "WARNING",
  "logger": "api_observable",
  "msg": "Product not found",
  "correlationId": "abc123-def456-ghi789",
  "product_id": "00000000-0000-0000-0000-000000000000"
}
```

```json
{
  "ts": "2025-11-26T13:45:22.465678Z",
  "level": "WARNING",
  "logger": "api_observable",
  "msg": "HTTP exception",
  "correlationId": "abc123-def456-ghi789",
  "status": 404,
  "error": "{'code': 'NOT_FOUND', 'msg': 'Product 00000000-0000-0000-0000-000000000000 not found'}"
}
```

```json
{
  "ts": "2025-11-26T13:45:22.467890Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Request completed",
  "correlationId": "abc123-def456-ghi789",
  "method": "GET",
  "path": "/api/v1/products/00000000-0000-0000-0000-000000000000",
  "status": 404,
  "latency_ms": 4.2,
  "userId": "user456"
}
```

**Análisis:**
- ⚠️ Level: WARNING (no CRITICAL porque es error esperado)
- ✅ correlationId permite trazar request completa
- ✅ Latency: 4.2ms (rápido incluso con error)
- ✅ product_id logged para debugging
- ℹ️ Status 404 = client error, no alerta crítica

---

## ⚠️ LOG 3: Error 409 (Version Conflict - Optimistic Locking)

```json
{
  "ts": "2025-11-26T13:50:10.123456Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Request started",
  "correlationId": "xyz789-abc123-def456",
  "method": "PUT",
  "path": "/api/v1/products/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "userId": "user789"
}
```

```json
{
  "ts": "2025-11-26T13:50:10.131234Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Trace step: updating_product",
  "correlationId": "xyz789-abc123-def456",
  "step": "updating_product",
  "elapsed_ms": 5.2
}
```

```json
{
  "ts": "2025-11-26T13:50:10.134567Z",
  "level": "WARNING",
  "logger": "api_observable",
  "msg": "Version conflict",
  "correlationId": "xyz789-abc123-def456",
  "product_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "error": "Version conflict: expected 1, got 2"
}
```

```json
{
  "ts": "2025-11-26T13:50:10.137890Z",
  "level": "WARNING",
  "logger": "api_observable",
  "msg": "HTTP exception",
  "correlationId": "xyz789-abc123-def456",
  "status": 409,
  "error": "{'code': 'CONFLICT', 'msg': 'Version conflict: expected 1, got 2'}"
}
```

```json
{
  "ts": "2025-11-26T13:50:10.140123Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Request completed",
  "correlationId": "xyz789-abc123-def456",
  "method": "PUT",
  "path": "/api/v1/products/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": 409,
  "latency_ms": 8.9,
  "userId": "user789"
}
```

**Análisis:**
- ⚠️ Status 409 = CONFLICT (optimistic locking funcionando)
- ✅ Error message claro: "expected 1, got 2"
- ✅ product_id presente para correlacionar con otros logs
- ℹ️ Si 409 es frecuente → indica alta concurrencia (bueno) o retry logic faltante (malo)

---

## ❌ LOG 4: Error 422 (Validation Error)

```json
{
  "ts": "2025-11-26T14:00:00.123456Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Request started",
  "correlationId": "validation-error-001",
  "method": "POST",
  "path": "/api/v1/products",
  "userId": "user999"
}
```

```json
{
  "ts": "2025-11-26T14:00:00.125678Z",
  "level": "WARNING",
  "logger": "api_observable",
  "msg": "HTTP exception",
  "correlationId": "validation-error-001",
  "status": 422,
  "error": "[{'type': 'value_error', 'loc': ('body', 'price'), 'msg': 'Input should be greater than or equal to 0', 'input': -10}]"
}
```

```json
{
  "ts": "2025-11-26T14:00:00.127890Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Request completed",
  "correlationId": "validation-error-001",
  "method": "POST",
  "path": "/api/v1/products",
  "status": 422,
  "latency_ms": 2.1,
  "userId": "user999"
}
```

**Análisis:**
- ⚠️ Status 422 = Unprocessable Entity (validación Pydantic)
- ✅ Error detallado: campo 'price', valor -10, regla 'ge=0'
- ✅ Latency ultra-baja: 2.1ms (validación rápida)
- ℹ️ Si 422 es >15% → frontend enviando datos incorrectos (alerta)

---

## 🔴 LOG 5: Error 500 (Internal Server Error)

```json
{
  "ts": "2025-11-26T14:30:00.123456Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Request started",
  "correlationId": "internal-error-001",
  "method": "POST",
  "path": "/api/v1/products",
  "userId": "user111"
}
```

```json
{
  "ts": "2025-11-26T14:30:00.145678Z",
  "level": "ERROR",
  "logger": "api_observable",
  "msg": "Request failed with exception",
  "correlationId": "internal-error-001",
  "method": "POST",
  "path": "/api/v1/products",
  "error": "division by zero"
}
```

```json
{
  "ts": "2025-11-26T14:30:00.147890Z",
  "level": "ERROR",
  "logger": "api_observable",
  "msg": "Unhandled exception",
  "correlationId": "internal-error-001",
  "error": "division by zero",
  "error_type": "ZeroDivisionError"
}
```

```json
{
  "ts": "2025-11-26T14:30:00.150123Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "Request completed",
  "correlationId": "internal-error-001",
  "method": "POST",
  "path": "/api/v1/products",
  "status": 500,
  "latency_ms": 14.5,
  "userId": "user111"
}
```

**Análisis:**
- 🔴 Level: ERROR (crítico, bug en código)
- 🔴 Status 500 = servidor culpable, no cliente
- ✅ error_type: "ZeroDivisionError" (útil para debugging)
- ✅ correlationId permite reproducir request exacta
- 🚨 Si 500 >0.1% → ALERTA CRÍTICA, rollback si deploy reciente

---

## 📊 LOG 6: Lifecycle Events (Startup/Shutdown)

**Startup:**
```json
{
  "ts": "2025-11-26T12:00:00.000000Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "API starting up",
  "service": "api_observable",
  "version": "1.0.0"
}
```

**Shutdown:**
```json
{
  "ts": "2025-11-26T18:00:00.000000Z",
  "level": "INFO",
  "logger": "api_observable",
  "msg": "API shutting down",
  "total_requests": 12543
}
```

**Análisis:**
- ℹ️ Eventos de lifecycle para auditoría
- ✅ Versión logged al startup (para tracking de deploys)
- ✅ Total de requests al shutdown (metrics summary)

---

## 🔍 QUERIES ÚTILES CON JQ

### 1. Filtrar solo errores (4xx y 5xx)

```bash
cat logs/api.log | jq 'select(.status >= 400)'
```

---

### 2. Contar errores por status code

```bash
cat logs/api.log | jq -s 'group_by(.status) | map({status: .[0].status, count: length}) | sort_by(.status)'
```

**Output:**
```json
[
  {"status": 200, "count": 9520},
  {"status": 201, "count": 1234},
  {"status": 204, "count": 567},
  {"status": 404, "count": 123},
  {"status": 409, "count": 45},
  {"status": 422, "count": 89},
  {"status": 500, "count": 2}
]
```

---

### 3. Ver requests de un usuario específico

```bash
cat logs/api.log | jq 'select(.userId == "user123")'
```

---

### 4. Calcular latencia promedio por endpoint

```bash
cat logs/api.log | jq -s '
  group_by(.path) | 
  map({
    endpoint: .[0].path, 
    avg_latency: (map(.latency_ms) | add / length)
  })
'
```

---

### 5. Trazar request completa por correlationId

```bash
cat logs/api.log | jq 'select(.correlationId == "550e8400-e29b-41d4-a716-446655440000")'
```

**Output:** Todos los logs de esa request (inicio, steps, completion)

---

### 6. Alertas: Requests con latencia > 50ms

```bash
cat logs/api.log | jq 'select(.latency_ms > 50) | {correlationId, path, latency_ms}'
```

---

### 7. Top 10 usuarios con más errores

```bash
cat logs/api.log | jq -s '
  map(select(.status >= 400)) | 
  group_by(.userId) | 
  map({user: .[0].userId, errors: length}) | 
  sort_by(.errors) | 
  reverse | 
  .[0:10]
'
```

---

## 📈 RETENTION POLICY (Producción)

### Configuración de Logrotate

```bash
# /etc/logrotate.d/api_observable
/var/log/api_observable/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload api_observable
    endscript
}
```

**Política:**
- **Daily rotation:** Nuevo archivo cada día
- **Retain 30 days:** Logs de último mes disponibles
- **Compress:** Archivos viejos en gzip (ahorra 80% espacio)
- **Create with permissions:** 0640 = solo owner/group leen

---

## 🔐 SENSITIVE DATA POLICY

### ❌ NUNCA loggear:

- Passwords
- JWT tokens completos (loggear solo últimos 4 chars: `...a1b2`)
- API keys
- Números de tarjeta de crédito
- Emails completos (usar `user***@domain.com`)
- Direcciones IP completas en prod (usar primeros 2 octetos: `192.168.*.*`)

### ✅ SÍ loggear:

- User IDs (UUID, no email)
- correlationIds
- Timestamps
- Status codes
- Latencias
- Endpoints
- Error messages (sin stack traces en prod)

---

**Conclusión:** Logs estructurados JSON permiten queries eficientes, alertas automáticas y debugging rápido. Combinados con dashboard de métricas, proporcionan observabilidad completa.

**Autor:** Ejercicio 5 - Semana 7 IA  
**Versión:** 1.0.0
