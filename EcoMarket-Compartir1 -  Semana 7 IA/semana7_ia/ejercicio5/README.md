# Ejercicio 5: Observabilidad Mínima Viable - API REST Observable

**Autor:** Ejercicio 5 - Semana 7 IA  
**Fecha:** 26 Nov 2025  
**Tema:** Logging estructurado, métricas, traces y dashboards para producción

---

## 📋 TABLA DE CONTENIDOS

1. [Descripción General](#-descripción-general)
2. [Arquitectura](#-arquitectura)
3. [Quickstart](#-quickstart)
4. [Features Implementadas](#-features-implementadas)
5. [Estructura del Proyecto](#-estructura-del-proyecto)
6. [Logging Estructurado](#-logging-estructurado)
7. [Métricas y KPIs](#-métricas-y-kpis)
8. [Request Tracing](#-request-tracing)
9. [Dashboard Live](#-dashboard-live)
10. [Alertas y Umbrales](#-alertas-y-umbrales)
11. [Troubleshooting](#-troubleshooting)
12. [Producción](#-producción)

---

## 🎯 DESCRIPCIÓN GENERAL

Este ejercicio implementa **observabilidad mínima viable (MVo)** para una API REST, proporcionando las herramientas esenciales para monitorear, debuggear y mantener una API en producción.

### Objetivos de Aprendizaje

1. **Structured Logging:** Logs en formato JSON para queries eficientes
2. **Metrics Collection:** Latencia (p50/p95/p99) y error rates por endpoint
3. **Request Tracing:** Pipeline completo request→response con timestamps
4. **Dashboard:** Visualización de métricas clave en tiempo real
5. **Alerting:** Umbrales críticos para detección temprana de problemas

### Principios de Observabilidad

**Los 3 Pilares:**
```
┌─────────────────────────────────────────────────────────┐
│ OBSERVABILITY = Logs + Metrics + Traces                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ LOGS      →  "Qué pasó" (events, errors)               │
│ METRICS   →  "Cómo está el sistema" (latency, errors)  │
│ TRACES    →  "Por qué es lento" (request pipeline)     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🏗️ ARQUITECTURA

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT (Browser/Mobile)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP Request
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               OBSERVABILITY MIDDLEWARE                      │
│  1. Generate correlationId                                  │
│  2. Create RequestTracer                                    │
│  3. Log "Request started"                                   │
│  4. Measure latency (start timer)                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    ENDPOINT (CRUD)                          │
│  tracer.add_step("validating_input")                        │
│  tracer.add_step("querying_database")                       │
│  tracer.add_step("product_created")                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               OBSERVABILITY MIDDLEWARE                      │
│  5. Calculate latency (stop timer)                          │
│  6. Record metrics (MetricsCollector)                       │
│  7. Log "Request completed"                                 │
│  8. Add headers (X-Correlation-Id, X-Latency-Ms)            │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP Response
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT                                   │
└─────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────┐
│                  OBSERVABILITY STACK                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ StructuredLogger│ MetricsCollector│ RequestTracer│     │
│  │                │  │              │  │              │     │
│  │ • JSON logs    │  │ • Latencies  │  │ • Steps      │     │
│  │ • correlationId│  │ • Error rates│  │ • Timestamps │     │
│  │ • ISO 8601 ts  │  │ • P50/95/99  │  │ • Details    │     │
│  └────────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│           │                 │                  │             │
│           └─────────────────┼──────────────────┘             │
│                             │                                │
│                             ▼                                │
│                    ┌────────────────┐                        │
│                    │ API Endpoints  │                        │
│                    ├────────────────┤                        │
│                    │ GET /_metrics  │ ← Dashboard queries    │
│                    │ GET /_trace    │ ← Debugging            │
│                    └────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 QUICKSTART

### Pre-requisitos

- Python 3.11+
- FastAPI, Uvicorn, Pydantic (ver requirements.txt)

### Instalación

```bash
cd semana7_ia/ejercicio5

# Instalar dependencias
pip install fastapi uvicorn pydantic requests
```

### Ejecución Rápida

```bash
# Terminal 1: Levantar API observable
uvicorn api_observable:app --reload --port 8000

# Output esperado:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# {"ts":"2025-11-26T13:42:15Z","level":"INFO","msg":"API starting up","service":"api_observable","version":"1.0.0"}
```

```bash
# Terminal 2: Generar tráfico de prueba
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -H "X-User-Id: user123" \
  -d '{"name": "iPhone 15 Pro", "price": 999, "currency": "USD"}'

# Ver logs estructurados en Terminal 1:
# {"ts":"...","level":"INFO","msg":"Request started","correlationId":"550e8400-...","method":"POST","path":"/api/v1/products","userId":"user123"}
# {"ts":"...","level":"INFO","msg":"Product created","correlationId":"550e8400-...","product_id":"a1b2c3d4-...","name":"iPhone 15 Pro"}
# {"ts":"...","level":"INFO","msg":"Request completed","correlationId":"550e8400-...","status":201,"latency_ms":12.34}
```

```bash
# Terminal 3: Dashboard en tiempo real
python dashboard_live.py

# Output:
# ================================================================================
# 🔍 OBSERVABILITY DASHBOARD - LIVE METRICS
# ================================================================================
# 📊 GLOBAL METRICS
# Total Requests:  15
# Throughput:      0.25 req/s
# 
# ⏱️  LATENCY & ERROR RATE PER ENDPOINT
# POST /api/v1/products    12.3ms  24.5ms  42.1ms  2.5%   0.0%
```

---

## ✨ FEATURES IMPLEMENTADAS

### 1. ✅ Logging Estructurado JSON

**Características:**
- Formato JSON por línea (parseable con `jq`, Elasticsearch)
- Timestamps ISO 8601 con timezone UTC
- correlationId en TODAS las logs de la misma request
- Campos estándar: ts, level, logger, msg, correlationId, path, method, status, latency_ms, userId

**Ejemplo de log:**
```json
{
  "ts": "2025-11-26T13:42:15.123456Z",
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

---

### 2. ✅ Métricas de Latencia (P50, P95, P99)

**Características:**
- Percentiles calculados por endpoint
- Historial de últimas 1000 requests por endpoint
- P50 (mediana), P95, P99 para identificar tail latency
- Contador de requests totales

**Query API:**
```bash
curl http://localhost:8000/api/v1/_metrics | jq '.data["POST /api/v1/products"].latency'

# Output:
# {
#   "p50": 12.34,
#   "p95": 24.56,
#   "p99": 42.12,
#   "count": 150
# }
```

---

### 3. ✅ Error Rate por Endpoint (4xx y 5xx)

**Características:**
- Tasa de error 4xx (client errors) y 5xx (server errors) separadas
- Contador de errores totales por status code
- Cálculo de porcentaje sobre total de requests

**Query API:**
```bash
curl http://localhost:8000/api/v1/_metrics | jq '.data["GET /api/v1/products/550e8400-e29b-41d4-a716-446655440000"].errors'

# Output:
# {
#   "error_rate_4xx": 8.0,
#   "error_rate_5xx": 0.1,
#   "total": 500,
#   "errors_4xx": 40,
#   "errors_5xx": 1
# }
```

---

### 4. ✅ Request Tracing (Pipeline Steps)

**Características:**
- Trace completo de pipeline request→response
- Timestamps relativos (ms desde inicio de request)
- Detalles customizados por paso (ej: product_id, name)
- Accesible en runtime via `/_trace` endpoint

**Ejemplo de trace:**
```bash
curl http://localhost:8000/api/v1/_trace | jq '.data.steps'

# Output:
# [
#   {
#     "step": "request_received",
#     "timestamp_ms": 0.12,
#     "details": {"method": "POST", "path": "/api/v1/products"}
#   },
#   {
#     "step": "validating_input",
#     "timestamp_ms": 3.45,
#     "details": {"name": "iPhone 15 Pro"}
#   },
#   {
#     "step": "product_created",
#     "timestamp_ms": 8.76,
#     "details": {"product_id": "a1b2c3d4-..."}
#   }
# ]
```

---

### 5. ✅ Dashboard CLI en Tiempo Real

**Características:**
- Actualización cada 5 segundos
- Métricas globales (total requests, uptime, throughput)
- Latencia por endpoint con barras visuales
- Colores ANSI (verde/amarillo/rojo según umbrales)
- Alertas activas destacadas

**Ejecutar:**
```bash
python dashboard_live.py
```

---

### 6. ✅ 3 Alertas con Umbrales Críticos

| Alerta | Umbral | Criticidad |
|--------|--------|------------|
| **High 5xx Rate** | >1% | 🔴 CRITICAL |
| **High Latency** | P95 >50ms | ⚠️ WARNING |
| **High 4xx Rate (POST)** | >15% | ⚠️ WARNING |

---

## 📁 ESTRUCTURA DEL PROYECTO

```
ejercicio5/
│
├── api_observable.py           # 🎯 API con observabilidad completa (650 líneas)
│   ├── StructuredLogger        # Logging JSON con custom formatter
│   ├── MetricsCollector         # Latencia + error rate por endpoint
│   ├── RequestTracer            # Pipeline tracing con timestamps
│   ├── observability_middleware # Instrumentación automática
│   └── Endpoints:
│       ├── CRUD /api/v1/products (mismos del Ejercicio 4)
│       ├── GET /api/v1/_metrics  (métricas agregadas)
│       ├── GET /api/v1/_trace    (trace de request actual)
│       ├── POST /_test/clear     (limpieza para tests)
│       └── GET /_test/stats      (estadísticas DB)
│
├── dashboard_live.py            # 📊 Dashboard CLI interactivo (150 líneas)
│   ├── render_dashboard()       # Loop cada 5s
│   ├── Métricas globales        # Total requests, uptime, throughput
│   ├── Latencia por endpoint    # P50/P95/P99 con barras ASCII
│   └── Alertas activas          # 🔴/⚠️ según umbrales
│
├── DASHBOARD.md                 # 📈 Especificación de 5 gráficos + 3 alertas
│   ├── Gráfico 1: Latency Percentiles (P50/P95/P99)
│   ├── Gráfico 2: Error Rate 4xx/5xx
│   ├── Gráfico 3: Request Throughput (req/s)
│   ├── Gráfico 4: Request Tracing (pipeline steps)
│   ├── Gráfico 5: Active Errors Stream (últimos 10)
│   └── 3 Alertas: High 5xx, High Latency, High 4xx (POST)
│
├── EJEMPLOS_LOGS.md             # 📝 Logs reales con análisis (500 líneas)
│   ├── LOG 1: Request exitosa (201 Created)
│   ├── LOG 2: Error 404 (Product Not Found)
│   ├── LOG 3: Error 409 (Version Conflict)
│   ├── LOG 4: Error 422 (Validation Error)
│   ├── LOG 5: Error 500 (Internal Server Error)
│   ├── LOG 6: Lifecycle events (startup/shutdown)
│   ├── Queries útiles con jq
│   └── Retention policy + sensitive data policy
│
├── CRITICA_Y_MEJORA.md          # 🔍 Análisis técnico (800 líneas)
│   ├── Fortalezas (5 secciones)
│   ├── Debilidades (7 secciones)
│   ├── Prompt mejorado v2 (production-grade)
│   └── Roadmap de implementación (5 fases)
│
└── README.md                    # 📖 Este archivo
    └── Documentación completa
```

---

## 📝 LOGGING ESTRUCTURADO

### Implementación

**StructuredLogger:**
```python
class StructuredLogger:
    def _json_formatter(self):
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                return json.dumps({
                    "ts": datetime.utcnow().isoformat() + "Z",
                    "level": record.levelname,
                    "msg": record.getMessage(),
                    "correlationId": getattr(record, 'correlationId', None),
                    "path": getattr(record, 'path', None),
                    # ... más campos
                })
```

### Uso en Endpoints

```python
@app.post("/api/v1/products")
def create_product(data: ProductCreate, request: Request):
    logger.info(
        "Product created",
        correlationId=request.state.correlation_id,
        product_id=str(product.id),
        name=product.name
    )
```

### Queries con jq

```bash
# 1. Filtrar solo errores
tail -f logs/api.log | jq 'select(.status >= 400)'

# 2. Contar errores por status code
cat logs/api.log | jq -s 'group_by(.status) | map({status: .[0].status, count: length})'

# 3. Requests de un usuario
cat logs/api.log | jq 'select(.userId == "user123")'

# 4. Latencia promedio por endpoint
cat logs/api.log | jq -s 'group_by(.path) | map({endpoint: .[0].path, avg_latency: (map(.latency_ms) | add / length)})'

# 5. Trazar request por correlationId
cat logs/api.log | jq 'select(.correlationId == "550e8400-...")'
```

Ver más ejemplos en **EJEMPLOS_LOGS.md**.

---

## 📊 MÉTRICAS Y KPIs

### MetricsCollector

**Estructura de datos:**
```python
class MetricsCollector:
    _latencies: Dict[str, deque]       # endpoint → [latency_ms, ...]
    _error_counts: Dict[str, Dict[int, int]]  # endpoint → {status_code: count}
    _request_counts: Dict[str, int]    # endpoint → total_requests
```

### Métricas Disponibles

1. **Latency Percentiles:**
   ```python
   {
     "p50": 12.34,  # 50% de requests son más rápidas
     "p95": 24.56,  # 95% de requests son más rápidas (SLA típico)
     "p99": 42.12,  # 99% de requests son más rápidas (tail latency)
     "count": 150
   }
   ```

2. **Error Rates:**
   ```python
   {
     "error_rate_4xx": 2.5,  # % de requests con 4xx
     "error_rate_5xx": 0.1,  # % de requests con 5xx
     "total": 500,
     "errors_4xx": 13,
     "errors_5xx": 1
   }
   ```

3. **Global Metrics:**
   ```python
   {
     "total_requests": 12543,
     "uptime_seconds": 3600,
     "requests_per_second": 3.48
   }
   ```

### Query API

```bash
# Todas las métricas
curl http://localhost:8000/api/v1/_metrics | jq

# Solo latencia de un endpoint
curl http://localhost:8000/api/v1/_metrics | \
  jq '.data["POST /api/v1/products"].latency'

# Endpoints con error rate > 5%
curl http://localhost:8000/api/v1/_metrics | \
  jq '.data | to_entries[] | select(.value.errors.error_rate_4xx > 5)'
```

---

## 🔍 REQUEST TRACING

### RequestTracer

**Implementación:**
```python
class RequestTracer:
    def __init__(self, correlation_id: str):
        self.correlation_id = correlation_id
        self.steps: List[Dict] = []
        self.start_time = time.perf_counter()
    
    def add_step(self, name: str, details: Optional[Dict] = None):
        elapsed_ms = (time.perf_counter() - self.start_time) * 1000
        self.steps.append({
            "step": name,
            "timestamp_ms": round(elapsed_ms, 2),
            "details": details or {}
        })
```

### Uso en Endpoints

```python
@app.get("/api/v1/products/{product_id}")
def get_product(product_id: uuid.UUID, request: Request):
    tracer = request.state.tracer
    
    tracer.add_step("querying_database", {"product_id": str(product_id)})
    product = db.get(product_id)
    
    if not product:
        tracer.add_step("product_not_found")
        raise HTTPException(status_code=404, ...)
    
    tracer.add_step("product_found", {"name": product.name})
    return {"data": product.model_dump(mode="json"), "error": None}
```

### Ver Trace

```bash
# Hacer request con header X-User-Id
curl -H "X-User-Id: user123" http://localhost:8000/api/v1/products | \
  jq '.data.items[0].id'

# Ver trace de esa request
curl http://localhost:8000/api/v1/_trace | jq '.data'

# Output:
# {
#   "correlationId": "550e8400-...",
#   "steps": [
#     {"step": "request_received", "timestamp_ms": 0.12, "details": {...}},
#     {"step": "querying_products_list", "timestamp_ms": 2.34, "details": {...}},
#     {"step": "products_retrieved", "timestamp_ms": 5.67, "details": {...}}
#   ]
# }
```

---

## 📈 DASHBOARD LIVE

### Ejecutar Dashboard

```bash
python dashboard_live.py
```

### Output Ejemplo

```
================================================================================
🔍 OBSERVABILITY DASHBOARD - LIVE METRICS
================================================================================
Timestamp: 2025-11-26 13:42:15
================================================================================

📊 GLOBAL METRICS
--------------------------------------------------------------------------------
  Total Requests:      1,543
  Uptime:               45 min 23 sec
  Throughput:            0.57 req/s

⏱️  LATENCY & ERROR RATE PER ENDPOINT
--------------------------------------------------------------------------------
Endpoint                                      P50      P95      P99      4xx%     5xx%
--------------------------------------------------------------------------------
POST /api/v1/products                        12.3ms   24.5ms   42.1ms   2.5%    0.0%
  └─ ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 24.5ms / 100ms
GET /api/v1/products/550e8400-e29b-41d4...   3.1ms    8.2ms   14.5ms   8.0%    0.1%
  └─ ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 8.2ms / 100ms

🚨 ACTIVE ALERTS
--------------------------------------------------------------------------------
  ⚠️  HIGH 4xx RATE: GET /api/v1/products/... has 8.0% validation errors (threshold: 5%)

================================================================================
Refreshing in 5s... (Press Ctrl+C to exit)
```

### Features

- ✅ Auto-refresh cada 5 segundos
- ✅ Colores ANSI (verde/amarillo/rojo)
- ✅ Barras ASCII de latencia
- ✅ Alertas destacadas en sección separada
- ✅ Métricas globales en header

---

## 🚨 ALERTAS Y UMBRALES

### Alerta 1: High 5xx Rate

**Definición:**
```python
if error_rate_5xx > 1.0:
    ALERT("CRITICAL: High server error rate")
```

**Umbral:** 1% de requests con 5xx

**Justificación:**
- 5xx = errores del servidor (bugs, DB down)
- 1% = ~10 errores cada 1000 requests
- Crítico porque afecta usuarios sin culpa de ellos

**Acción:**
- 🔔 Notificar a on-call engineer
- 🔍 Revisar logs: `tail -f logs/api.log | grep 'status":5'`
- 🛠️ Rollback si deploy reciente
- 📊 Verificar health de DB/dependencies

---

### Alerta 2: High Latency (P95)

**Definición:**
```python
if latency_p95 > 50.0:
    ALERT("WARNING: High latency detected")
```

**Umbral:** P95 > 50ms

**Justificación:**
- P95 = 95% de usuarios experimentan latencia < 50ms
- 50ms = umbral de "fast" según Google Web Vitals
- Si P95 > 50ms, 5% de usuarios tienen mala experiencia

**Acción:**
- 📊 Ver trace: `curl http://localhost:8000/api/v1/_trace`
- 🔎 Identificar paso lento (DB query, external API)
- 🗄️ Revisar slow queries (si DB real)
- 🚀 Optimizar código del endpoint

---

### Alerta 3: High 4xx Rate on CREATE

**Definición:**
```python
if endpoint == "POST /products" and error_rate_4xx > 15.0:
    ALERT("WARNING: High validation error rate on CREATE")
```

**Umbral:** 15% de requests con 4xx en POST /products

**Justificación:**
- POST /products = endpoint crítico
- 15% = 1 de cada 7 requests falla por validación
- Indica problemas en cliente (frontend)

**Acción:**
- 📱 Notificar a equipo frontend
- 📋 Revisar últimos errores: `tail logs/api.log | grep 'POST.*products.*422'`
- 📝 Documentar errores comunes en docs
- 🔧 Mejorar mensajes de error

---

## 🐛 TROUBLESHOOTING

### Problema 1: Dashboard No Se Conecta

**Síntoma:**
```
❌ ERROR: No se pudo conectar a la API
Detalle: Connection refused
```

**Solución:**
```bash
# 1. Verificar que API está corriendo
curl http://localhost:8000/

# 2. Si no responde, levantar API:
uvicorn api_observable:app --reload --port 8000

# 3. Verificar puerto correcto en dashboard_live.py:
API_BASE_URL = "http://localhost:8000"  # Debe coincidir
```

---

### Problema 2: Logs No Aparecen en Archivo

**Síntoma:**
```bash
cat logs/api.log
# cat: logs/api.log: No such file or directory
```

**Causa:** Implementación actual solo loggea a stdout.

**Solución temporal:**
```bash
# Redirigir stdout a archivo
uvicorn api_observable:app --reload --port 8000 > logs/api.log 2>&1 &
```

**Solución permanente (Producción):**
```python
# En api_observable.py, agregar FileHandler:
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "logs/api.log",
    maxBytes=100_000_000,  # 100 MB
    backupCount=10
)
logger.logger.addHandler(handler)
```

---

### Problema 3: Métricas Se Resetean al Reiniciar API

**Síntoma:**
```bash
# Antes de restart: total_requests = 1543
# Después de restart: total_requests = 0
```

**Causa:** Métricas en memoria (no persisten).

**Solución (Desarrollo):** Aceptar limitación, es esperado.

**Solución (Producción):** Migrar a Prometheus (persistent storage).

---

### Problema 4: Dashboard Muestra "No endpoints with traffic yet"

**Síntoma:**
```
⏱️  LATENCY & ERROR RATE PER ENDPOINT
---------------------------------------------
  No endpoints with traffic yet...
```

**Causa:** No se han hecho requests a la API desde el último restart.

**Solución:**
```bash
# Generar tráfico de prueba
for i in {1..10}; do
  curl -s -X POST http://localhost:8000/api/v1/products \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"Product $i\", \"price\": $((100 + i)), \"currency\": \"USD\"}" > /dev/null
done

# Ahora dashboard mostrará métricas
```

---

### Problema 5: Colores No Se Ven en Windows PowerShell

**Síntoma:**
```
[91m HIGH LATENCY [0m  ← Códigos ANSI visibles
```

**Causa:** PowerShell 5.1 no soporta ANSI por defecto.

**Solución 1: Usar Windows Terminal (recomendado)**
```powershell
# Instalar Windows Terminal desde Microsoft Store
# Ejecutar dashboard_live.py en Windows Terminal
```

**Solución 2: PowerShell 7+**
```powershell
# Instalar PowerShell 7:
winget install Microsoft.PowerShell

# Ejecutar dashboard en PowerShell 7
pwsh
python dashboard_live.py
```

---

## 🚀 PRODUCCIÓN

### Migración a Stack Production-Grade

**Recomendado: Prometheus + Grafana + Loki**

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
  
  loki:
    image: grafana/loki
    ports:
      - "3100:3100"
```

---

### Logging con Rotation

```python
# Agregar en api_observable.py
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "logs/api.log",
    maxBytes=100_000_000,  # 100 MB
    backupCount=10         # Mantener 10 archivos = 1 GB
)
logger.logger.addHandler(handler)
```

---

### Sampling de Logs (Alto Tráfico)

```python
import random

# En observability_middleware:
sample_rate = 0.01  # 1% de tráfico exitoso

if response.status_code >= 400 or random.random() < sample_rate:
    # Solo loggear errores y 1% de requests exitosas
    logger.info("Request completed", ...)
```

---

### Alertas con Webhooks

```python
def send_slack_alert(message: str):
    import requests
    requests.post(
        "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
        json={"text": message}
    )

# En MetricsCollector:
if error_rate_5xx > 1.0:
    send_slack_alert(f"🔴 CRITICAL: {endpoint} has {error_rate_5xx}% 5xx errors")
```

---

### Métricas con Prometheus Client

```python
from prometheus_client import Histogram, Counter, generate_latest

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint", "status"]
)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

# En middleware:
REQUEST_LATENCY.labels(method=method, endpoint=endpoint, status=status).observe(latency)
REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()

# Endpoint para Prometheus scraping:
@app.get("/metrics")
def prometheus_metrics():
    return Response(content=generate_latest(), media_type="text/plain")
```

---

## 📚 RECURSOS ADICIONALES

### Archivos del Proyecto
- **DASHBOARD.md:** 5 gráficos esenciales + 3 alertas con umbrales
- **EJEMPLOS_LOGS.md:** Logs reales con análisis y queries jq
- **CRITICA_Y_MEJORA.md:** Análisis técnico + prompt v2 production-grade

### Documentación Externa
- [Google SRE Book - Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/#xref_monitoring_golden-signals)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)

### Comandos Útiles

```bash
# Ver logs en tiempo real con filtro
tail -f logs/api.log | jq 'select(.status >= 400)'

# Contar requests por endpoint
cat logs/api.log | jq -s 'group_by(.path) | map({endpoint: .[0].path, count: length})'

# Top 10 requests más lentas
cat logs/api.log | jq -s 'sort_by(.latency_ms) | reverse | .[0:10] | .[] | {path, latency_ms, correlationId}'

# Ver métricas formateadas
curl -s http://localhost:8000/api/v1/_metrics | jq '.data | to_entries[] | select(.key != "_global")'

# Generar tráfico de prueba
for i in {1..100}; do
  curl -s -X POST http://localhost:8000/api/v1/products \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"Product $i\", \"price\": $((100 + i)), \"currency\": \"USD\"}" &
done
```

---

## 🎓 CONCLUSIÓN

Este ejercicio demuestra:

1. ✅ **Logging estructurado JSON:** Parseable, consistente, con correlationId
2. ✅ **Métricas de latencia:** P50/P95/P99 por endpoint
3. ✅ **Error rates:** Separación de 4xx (cliente) y 5xx (servidor)
4. ✅ **Request tracing:** Pipeline completo con timestamps
5. ✅ **Dashboard live:** Visualización en tiempo real con alertas
6. ✅ **Instrumentación automática:** Middleware centralizado (zero boilerplate)

### Próximos Pasos

- Migrar métricas a **Prometheus** (persistent storage)
- Agregar **RotatingFileHandler** para logs
- Implementar **OpenTelemetry** para distributed tracing
- Crear **Grafana dashboards** con historical data
- Configurar **alertas con webhooks** (Slack, PagerDuty)

---

**¿Preguntas o problemas?**
- Revisar **Troubleshooting** section
- Ver **EJEMPLOS_LOGS.md** para queries jq
- Consultar **CRITICA_Y_MEJORA.md** para production migration

---

**Autor:** Ejercicio 5 - Semana 7 IA  
**Licencia:** MIT (uso académico)  
**Versión:** 1.0.0 (26 Nov 2025)
