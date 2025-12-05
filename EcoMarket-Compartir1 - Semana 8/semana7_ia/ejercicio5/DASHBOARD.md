# Dashboard de Observabilidad - Ejercicio 5

**Autor:** Ejercicio 5 - Semana 7 IA  
**Fecha:** 26 Nov 2025  
**Tema:** Observabilidad mínima viable con logs, métricas y traces

---

## 📊 DASHBOARD: 5 GRÁFICOS IMPRESCINDIBLES

### 1. **Latency por Endpoint (Percentiles P50/P95/P99)**

```
┌─────────────────────────────────────────────────────────────┐
│ Latencia de Endpoints (ms)                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ POST /products     ████████░░░░░░░░░░░░░░░░░  12ms (p50)  │
│                    ████████████████████░░░░░░  24ms (p95)  │
│                    ████████████████████████░░  42ms (p99)  │
│                                                             │
│ GET /products/:id  ███░░░░░░░░░░░░░░░░░░░░░░   3ms (p50)  │
│                    ████████░░░░░░░░░░░░░░░░░   8ms (p95)  │
│                    ██████████████░░░░░░░░░░░  14ms (p99)  │
│                                                             │
│ PUT /products/:id  ████████░░░░░░░░░░░░░░░░░   8ms (p50)  │
│                    ████████████████████░░░░░  17ms (p95)  │
│                    ████████████████████████░  31ms (p99)  │
│                                                             │
│ DELETE /products   ████░░░░░░░░░░░░░░░░░░░░░   4ms (p50)  │
│                    ██████████░░░░░░░░░░░░░░░  10ms (p95)  │
│                    ████████████████████░░░░░  18ms (p99)  │
│                                                             │
│ GET /products      █████░░░░░░░░░░░░░░░░░░░░   5ms (p50)  │
│                    ████████████░░░░░░░░░░░░░  12ms (p95)  │
│                    ██████████████████████░░░  21ms (p99)  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Propósito:**
- Detectar endpoints lentos (p99 > 50ms)
- Identificar degradación de performance
- Comparar latencia entre operaciones (READ vs WRITE)

**Consulta API:**
```bash
curl http://localhost:8000/api/v1/_metrics | jq '.data | to_entries[] | select(.key != "_global") | {endpoint: .key, latency: .value.latency}'
```

**Output esperado:**
```json
{
  "endpoint": "POST /api/v1/products",
  "latency": {
    "p50": 12.34,
    "p95": 24.56,
    "p99": 42.12,
    "count": 150
  }
}
```

---

### 2. **Error Rate por Endpoint (4xx y 5xx)**

```
┌─────────────────────────────────────────────────────────────┐
│ Tasa de Errores (%)                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ POST /products      ██░░░░░░░░░░░  2.5% (4xx)              │
│                     ░░░░░░░░░░░░░  0.0% (5xx)  ✅ Healthy  │
│                                                             │
│ GET /products/:id   ████████░░░░░  8.0% (4xx)  ⚠️ High     │
│                     ░░░░░░░░░░░░░  0.1% (5xx)              │
│                                                             │
│ PUT /products/:id   ████░░░░░░░░░  4.2% (4xx)              │
│                     ░░░░░░░░░░░░░  0.0% (5xx)  ✅ Healthy  │
│                                                             │
│ DELETE /products    ██░░░░░░░░░░░  2.0% (4xx)              │
│                     ░░░░░░░░░░░░░  0.0% (5xx)  ✅ Healthy  │
│                                                             │
│ GET /products       ░░░░░░░░░░░░░  0.5% (4xx)  ✅ Healthy  │
│                     ░░░░░░░░░░░░░  0.0% (5xx)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Propósito:**
- Identificar endpoints problemáticos (alta tasa de 404, 409, 500)
- Diferenciar errores de cliente (4xx) vs servidor (5xx)
- Alertar si 5xx > 1% (degradación del servicio)

**Consulta API:**
```bash
curl http://localhost:8000/api/v1/_metrics | jq '.data | to_entries[] | select(.key != "_global") | {endpoint: .key, errors: .value.errors}'
```

**Output esperado:**
```json
{
  "endpoint": "GET /api/v1/products/550e8400-e29b-41d4-a716-446655440000",
  "errors": {
    "error_rate_4xx": 8.0,
    "error_rate_5xx": 0.1,
    "total": 500,
    "errors_4xx": 40,
    "errors_5xx": 1
  }
}
```

---

### 3. **Request Throughput (Requests/Second)**

```
┌─────────────────────────────────────────────────────────────┐
│ Throughput Global                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  250 │                             ╭─╮                      │
│  200 │                       ╭─────╯ ╰─╮                    │
│  150 │               ╭───────╯         ╰──╮                 │
│  100 │         ╭─────╯                    ╰──╮              │
│   50 │   ╭─────╯                              ╰────╮        │
│    0 │───╯                                         ╰────────│
│      └───────────────────────────────────────────────────┘ │
│        00:00  00:15  00:30  00:45  01:00  01:15  01:30    │
│                                                             │
│  Current: 209.5 req/s                                      │
│  Peak:    245.8 req/s (00:42)                              │
│  Average: 187.3 req/s                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Propósito:**
- Monitorear carga de la API
- Detectar picos de tráfico
- Capacidad de planning (escalamiento horizontal)

**Consulta API:**
```bash
curl http://localhost:8000/api/v1/_metrics | jq '.data._global'
```

**Output esperado:**
```json
{
  "total_requests": 12543,
  "uptime_seconds": 3600,
  "requests_per_second": 3.48
}
```

---

### 4. **Request Tracing (Pipeline Visualization)**

```
┌─────────────────────────────────────────────────────────────┐
│ Request Trace: POST /api/v1/products                        │
│ Correlation ID: 550e8400-e29b-41d4-a716-446655440000       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  0ms   │ request_received                                  │
│        │ ├─ method: POST                                   │
│        │ ├─ path: /api/v1/products                         │
│        │ └─ client_ip: 127.0.0.1                           │
│        │                                                    │
│  2ms   │ processing_request                                │
│        │                                                    │
│  3ms   │ validating_input                                  │
│        │ └─ name: "iPhone 15 Pro"                          │
│        │                                                    │
│  8ms   │ product_created                                   │
│        │ └─ product_id: a1b2c3d4-...                       │
│        │                                                    │
│  9ms   │ response_generated                                │
│        │ └─ status: 201                                    │
│        │                                                    │
│  12ms  │ request_completed                                 │
│        │ └─ latency_ms: 12.34                              │
│        │                                                    │
└─────────────────────────────────────────────────────────────┘
```

**Propósito:**
- Debugging de requests lentas (identificar paso lento)
- Auditoría de requests (quién hizo qué y cuándo)
- Correlacionar múltiples requests (distributed tracing)

**Consulta API:**
```bash
curl -H "X-User-Id: user123" http://localhost:8000/api/v1/_trace | jq '.data'
```

**Output esperado:**
```json
{
  "correlationId": "550e8400-e29b-41d4-a716-446655440000",
  "steps": [
    {
      "step": "request_received",
      "timestamp_ms": 0.12,
      "details": {
        "method": "POST",
        "path": "/api/v1/products",
        "client_ip": "127.0.0.1"
      }
    },
    {
      "step": "validating_input",
      "timestamp_ms": 3.45,
      "details": {
        "name": "iPhone 15 Pro"
      }
    },
    {
      "step": "product_created",
      "timestamp_ms": 8.76,
      "details": {
        "product_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
      }
    }
  ]
}
```

---

### 5. **Active Errors Stream (Últimos 10 Errores)**

```
┌─────────────────────────────────────────────────────────────┐
│ Error Stream (Live)                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ [13:42:15] ❌ 404 NOT_FOUND                                │
│   GET /api/v1/products/00000000-0000-0000-0000-000000000000│
│   correlation_id: abc123...                                │
│   latency: 4.2ms                                           │
│   user_id: user456                                         │
│                                                             │
│ [13:41:58] ⚠️  409 CONFLICT                                │
│   PUT /api/v1/products/a1b2c3d4-...                        │
│   correlation_id: def456...                                │
│   error: "Version conflict: expected 1, got 2"             │
│   latency: 8.9ms                                           │
│                                                             │
│ [13:41:32] ❌ 422 VALIDATION_ERROR                         │
│   POST /api/v1/products                                    │
│   correlation_id: ghi789...                                │
│   error: "price must be >= 0"                              │
│   latency: 2.1ms                                           │
│                                                             │
│ [13:40:45] ❌ 400 BAD_REQUEST                              │
│   POST /api/v1/products                                    │
│   correlation_id: jkl012...                                │
│   error: "Tags must be unique"                             │
│   latency: 3.5ms                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Propósito:**
- Detección temprana de problemas
- Debugging en tiempo real
- Correlación de errores (múltiples 409 → problema de concurrencia)

**Ver logs en tiempo real:**
```bash
# Filtrar solo errores (4xx y 5xx)
tail -f logs/api.log | grep -E '"status":(4|5)[0-9]{2}'

# Con jq para formato legible:
tail -f logs/api.log | jq 'select(.status >= 400)'
```

**Output esperado:**
```json
{
  "ts": "2025-11-26T13:42:15.123456Z",
  "level": "WARNING",
  "logger": "api_observable",
  "msg": "Product not found",
  "correlationId": "abc123-def456-ghi789",
  "path": "/api/v1/products/00000000-0000-0000-0000-000000000000",
  "method": "GET",
  "status": 404,
  "latency_ms": 4.2,
  "userId": "user456"
}
```

---

## 🚨 3 ALERTAS CON UMBRALES

### Alerta 1: **High Error Rate (5xx)**

**Condición:**
```python
if error_rate_5xx > 1.0:
    ALERT("CRITICAL: High server error rate")
```

**Umbral:** 1% de requests con 5xx

**Justificación:**
- 5xx = errores del servidor (bugs, DB down, timeout)
- 1% = ~10 errores cada 1000 requests
- Crítico porque afecta a usuarios sin culpa de ellos

**Query de monitoreo:**
```bash
# Verificar tasa de 5xx global
curl http://localhost:8000/api/v1/_metrics | \
  jq '[.data | to_entries[] | select(.key != "_global") | .value.errors.error_rate_5xx] | max'

# Si retorna > 1.0 → ALERT
```

**Acción al dispararse:**
- 🔔 Slack/PagerDuty notification
- 📧 Email a equipo de SRE
- 🔍 Revisar logs con `tail -f logs/api.log | grep 'status":5'`
- 🛠️ Rollback si deploy reciente

---

### Alerta 2: **High Latency (P95 > 50ms)**

**Condición:**
```python
if latency_p95 > 50.0:
    ALERT("WARNING: High latency detected")
```

**Umbral:** P95 > 50ms

**Justificación:**
- P95 = 95% de usuarios experimentan latencia < 50ms
- 50ms = umbral de "fast" según Google Web Vitals
- Si P95 > 50ms, 5% de usuarios tienen mala experiencia

**Query de monitoreo:**
```bash
# Verificar P95 por endpoint
curl http://localhost:8000/api/v1/_metrics | \
  jq '.data | to_entries[] | select(.key != "_global") | select(.value.latency.p95 > 50) | {endpoint: .key, p95: .value.latency.p95}'
```

**Acción al dispararse:**
- 📊 Revisar dashboard de latencia
- 🔎 Identificar endpoint lento con `/api/v1/_trace`
- 🗄️ Verificar slow queries (si DB real)
- 🚀 Optimizar código del endpoint crítico

---

### Alerta 3: **High 4xx Rate on Critical Endpoint (POST /products)**

**Condición:**
```python
if endpoint == "POST /products" and error_rate_4xx > 15.0:
    ALERT("WARNING: High validation error rate on CREATE")
```

**Umbral:** 15% de requests con 4xx en POST /products

**Justificación:**
- POST /products = endpoint crítico (creación de recursos)
- 15% 4xx = 1 de cada 7 requests falla por validación
- Indica problemas en cliente (frontend enviando datos inválidos)

**Query de monitoreo:**
```bash
# Verificar tasa de 4xx en POST /products
curl http://localhost:8000/api/v1/_metrics | \
  jq '.data["POST /api/v1/products"].errors.error_rate_4xx'

# Si retorna > 15.0 → ALERT
```

**Acción al dispararse:**
- 📱 Notificar a equipo frontend
- 📋 Revisar últimos errores: `tail logs/api.log | grep 'POST.*products.*422'`
- 📝 Documentar errores comunes en Swagger/docs
- 🔧 Mejorar mensajes de error para cliente

---

## 🎨 IMPLEMENTACIÓN DEL DASHBOARD

### Opción 1: Grafana + Prometheus (Producción)

**Stack:**
```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
  
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

**prometheus.yml:**
```yaml
scrape_configs:
  - job_name: 'api_observable'
    scrape_interval: 15s
    metrics_path: '/api/v1/_metrics'
    static_configs:
      - targets: ['api:8000']
```

**Grafana dashboard:** Importar JSON con 5 gráficos definidos arriba.

---

### Opción 2: Script Python Simple (Desarrollo)

```python
#!/usr/bin/env python3
"""
Dashboard CLI simple para desarrollo
Uso: python dashboard.py
"""

import requests
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_dashboard():
    clear_screen()
    
    response = requests.get("http://localhost:8000/api/v1/_metrics")
    data = response.json()["data"]
    
    print("=" * 70)
    print("🔍 OBSERVABILITY DASHBOARD".center(70))
    print("=" * 70)
    print()
    
    # Global metrics
    global_data = data.get("_global", {})
    print(f"📊 Total Requests: {global_data.get('total_requests', 0)}")
    print(f"⏱️  Uptime: {global_data.get('uptime_seconds', 0)}s")
    print(f"🚀 Throughput: {global_data.get('requests_per_second', 0)} req/s")
    print()
    
    # Latency por endpoint
    print("⏱️  LATENCY (ms)")
    print("-" * 70)
    
    for endpoint, metrics in data.items():
        if endpoint == "_global":
            continue
        
        latency = metrics.get("latency", {})
        errors = metrics.get("errors", {})
        
        p50 = latency.get("p50", 0)
        p95 = latency.get("p95", 0)
        p99 = latency.get("p99", 0)
        
        error_4xx = errors.get("error_rate_4xx", 0)
        error_5xx = errors.get("error_rate_5xx", 0)
        
        # Alerta si p95 > 50ms
        alert = "⚠️ " if p95 > 50 else "✅"
        
        print(f"{alert} {endpoint[:50]:<50} p50:{p50:>6.1f} p95:{p95:>6.1f} p99:{p99:>6.1f}")
        
        # Mostrar errores si > 0
        if error_4xx > 0 or error_5xx > 0:
            print(f"   └─ Errors: {error_4xx:.1f}% (4xx), {error_5xx:.1f}% (5xx)")
    
    print()
    print("Refreshing in 5s... (Ctrl+C to exit)")

if __name__ == "__main__":
    try:
        while True:
            render_dashboard()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\nDashboard stopped.")
```

**Uso:**
```bash
# Terminal 1: API corriendo
uvicorn api_observable:app --reload

# Terminal 2: Dashboard live
python dashboard.py
```

---

### Opción 3: curl + jq (Quickest)

```bash
#!/bin/bash
# dashboard.sh - Dashboard en una sola línea

watch -n 5 'curl -s http://localhost:8000/api/v1/_metrics | jq -r "
  .data | 
  to_entries[] | 
  select(.key != \"_global\") | 
  \"\(.key): p95=\(.value.latency.p95)ms, errors=\(.value.errors.error_rate_4xx)% (4xx) + \(.value.errors.error_rate_5xx)% (5xx)\"
"'
```

**Output:**
```
POST /api/v1/products: p95=24.5ms, errors=2.5% (4xx) + 0.0% (5xx)
GET /api/v1/products/550e8400-e29b-41d4-a716-446655440000: p95=8.2ms, errors=8.0% (4xx) + 0.1% (5xx)
...
```

---

## 📋 CHECKLIST DE OBSERVABILIDAD

Antes de deployment a producción, verificar:

- [ ] **Logging estructurado:** Todos los logs en formato JSON
- [ ] **Correlation ID:** Presente en logs y headers (`X-Correlation-Id`)
- [ ] **Latency tracking:** P50, P95, P99 medidos por endpoint
- [ ] **Error tracking:** Tasas de 4xx y 5xx calculadas
- [ ] **Request tracing:** Pipeline completo visible con `/_trace`
- [ ] **Alertas configuradas:** 3 alertas críticas funcionando
- [ ] **Dashboard accessible:** Grafana o CLI dashboard corriendo
- [ ] **Log rotation:** Logs no llenan disco (logrotate configurado)
- [ ] **Metrics retention:** Prometheus retiene métricas por 30 días
- [ ] **Sensitive data:** No loggear passwords, tokens, PII

---

## 🔥 DEMO RÁPIDO

### 1. Levantar API
```bash
cd semana7_ia/ejercicio5
uvicorn api_observable:app --reload --port 8000
```

### 2. Generar tráfico
```bash
# Crear 10 productos
for i in {1..10}; do
  curl -s -X POST http://localhost:8000/api/v1/products \
    -H "Content-Type: application/json" \
    -H "X-User-Id: user$i" \
    -d "{\"name\": \"Product $i\", \"price\": $((100 + i)), \"currency\": \"USD\"}" > /dev/null
done

# Generar algunos errores 404
curl -s http://localhost:8000/api/v1/products/00000000-0000-0000-0000-000000000000 > /dev/null
```

### 3. Ver logs estructurados
```bash
# Ver últimos 5 logs
curl -s http://localhost:8000/api/v1/products | head -5

# Output esperado (JSON por línea):
# {"ts":"2025-11-26T13:42:15Z","level":"INFO","msg":"Request started","correlationId":"abc123...","method":"GET","path":"/api/v1/products"}
```

### 4. Ver métricas
```bash
curl http://localhost:8000/api/v1/_metrics | jq
```

### 5. Ver trace de request actual
```bash
curl http://localhost:8000/api/v1/_trace | jq '.data.steps'
```

---

**Conclusión:** Este dashboard proporciona las **5 visualizaciones esenciales** y **3 alertas críticas** para observabilidad mínima viable. Escalable a Grafana/Prometheus para producción.

**Autor:** Ejercicio 5 - Semana 7 IA  
**Versión:** 1.0.0
