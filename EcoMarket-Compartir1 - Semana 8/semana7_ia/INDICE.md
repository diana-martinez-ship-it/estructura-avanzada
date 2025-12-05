# Semana 7 IA - Índice de Actividades

**Autor:** Actividades de IA - Semana 7  
**Fecha:** 26 Nov 2025  
**Tema:** Programación del lado del servidor con asistencia de IA

---

## 📋 ÍNDICE GENERAL

| Ejercicio | Tema | Archivos | Estado |
|-----------|------|----------|--------|
| [Ejercicio 1](#ejercicio-1-esqueleto-de-api--contratos) | API Skeleton + OpenAPI | 7 | ✅ |
| [Ejercicio 2](#ejercicio-2-middleware-de-autenticación--rate-limiting) | JWT + Rate Limiting + RBAC | 6 | ✅ |
| [Ejercicio 3](#ejercicio-3-validación-y-serialización-deterministas) | Validation + Serialization | 6 | ✅ |
| [Ejercicio 4](#ejercicio-4-pruebas-de-integración-e2e) | E2E Integration Testing | 6 | ✅ |
| [Ejercicio 5](#ejercicio-5-observabilidad-mínima-viable) | Logs + Metrics + Traces | 6 | ✅ |

**Total:** 5 ejercicios completos, 31 archivos, ~11,000 líneas de código y documentación

---

## 🎯 EJERCICIO 1: Esqueleto de API + Contratos

**Directorio:** `semana7_ia/ejercicio1/`

**Objetivo:** Diseñar una API REST con validación robusta, contratos de datos y documentación OpenAPI.

### Archivos Entregables

| Archivo | Líneas | Descripción |
|---------|--------|-------------|
| `dtos.py` | 120 | DTOs con Pydantic (ProductCreate, ProductUpdate, Product) |
| `api.py` | 280 | API REST con endpoints CRUD + validación |
| `openapi.yaml` | 150 | Especificación OpenAPI 3.0 completa |
| `test_api.py` | 250 | 18 tests (happy paths + edge cases) |
| `CRITICA_Y_MEJORA.md` | 680 | Análisis técnico + prompt mejorado v2 |
| `README.md` | 520 | Documentación con quickstart |

**Total:** 7 archivos, ~2,000 líneas

### Features Destacadas
- ✅ Validación con Pydantic (tipos, rangos, formatos)
- ✅ Error handling uniforme (formato JSON estándar)
- ✅ OpenAPI 3.0 con schemas y ejemplos
- ✅ Tests unitarios con pytest
- ✅ Sanitización XSS/SQLi básica

### Quickstart
```bash
cd semana7_ia/ejercicio1
uvicorn api:app --reload --port 8000
python test_api.py
```

---

## 🔐 EJERCICIO 2: Middleware de Autenticación + Rate Limiting

**Directorio:** `semana7_ia/ejercicio2/`

**Objetivo:** Implementar JWT authentication, rate limiting y RBAC para proteger endpoints.

### Archivos Entregables

| Archivo | Líneas | Descripción |
|---------|--------|-------------|
| `diagrama_pipeline.py` | 180 | Diagrama ASCII del pipeline de seguridad |
| `api_secure.py` | 450 | API con JWT, rate limiting y RBAC |
| `TABLA_ERRORES.md` | 280 | Tabla de respuestas 401/403/429 con ejemplos |
| `test_security.py` | 220 | 6 tests (3 success + 3 failure) |
| `CRITICA_Y_MEJORA.md` | 720 | Análisis técnico + prompt mejorado v2 |
| `README.md` | 580 | Documentación con troubleshooting |

**Total:** 6 archivos, ~2,430 líneas

### Features Destacadas
- ✅ JWT tokens (HS256) con expiration 15 min
- ✅ Refresh tokens en cookies httpOnly
- ✅ Rate limiting: 100 req/15min por IP, 1000 req/15min por userId
- ✅ RBAC: roles admin/user
- ✅ Logs estructurados con correlationId

### Quickstart
```bash
cd semana7_ia/ejercicio2
uvicorn api_secure:app --reload --port 8000
python test_security.py
```

---

## ✓ EJERCICIO 3: Validación y Serialización Deterministas

**Directorio:** `semana7_ia/ejercicio3/`

**Objetivo:** Definir esquemas JSON con reglas estrictas y serialización consistente.

### Archivos Entregables

| Archivo | Líneas | Descripción |
|---------|--------|-------------|
| `schemas.json` | 180 | JSON Schema Draft-07 para Product |
| `validators.py` | 320 | Validadores con reglas de negocio |
| `TABLA_ERRORES.md` | 380 | Tabla de errores por regla violada |
| `fuzzing_tests.py` | 280 | 10 fuzzing cases + boundary tests |
| `CRITICA_Y_MEJORA.md` | 750 | Análisis técnico + prompt mejorado v2 |
| `README.md` | 590 | Documentación con ejemplos |

**Total:** 6 archivos, ~2,500 líneas

### Features Destacadas
- ✅ JSON Schema Draft-07 completo
- ✅ Validadores: price ≥0, currency ∈{MXN,USD,EUR}, name 2-80 chars
- ✅ Serialización ordenada (sin nulls)
- ✅ Fuzzing: Unicode, límites, inyección SQL/XSS
- ✅ Tabla de errores con códigos consistentes

### Quickstart
```bash
cd semana7_ia/ejercicio3
python validators.py
python fuzzing_tests.py
```

---

## 🧪 EJERCICIO 4: Pruebas de Integración E2E

**Directorio:** `semana7_ia/ejercicio4/`

**Objetivo:** Tests E2E con fixtures, matriz de casos y métricas de cobertura.

### Archivos Entregables

| Archivo | Líneas | Descripción |
|---------|--------|-------------|
| `api_complete.py` | 450 | API con CRUD + optimistic locking |
| `test_e2e.py` | 560 | 48 test cases (16 funciones, 6 clases) |
| `MATRIZ_CASOS.md` | 580 | Documentación de 48 casos + coverage |
| `SCRIPTS_CURL.md` | 680 | Testing manual (Bash + PowerShell) |
| `CRITICA_Y_MEJORA.md` | 780 | Análisis técnico + prompt mejorado v2 |
| `README.md` | 850 | Documentación completa |

**Total:** 6 archivos, ~3,900 líneas

### Features Destacadas
- ✅ 48 test cases: CRUD, validación, concurrencia, edge cases
- ✅ Optimistic locking con version field
- ✅ Fixtures con autouse (aislamiento transaccional)
- ✅ Latency measurements (p50, p95, p99)
- ✅ 100% endpoint coverage, 95.6% code coverage

### Quickstart
```bash
cd semana7_ia/ejercicio4
# Terminal 1:
uvicorn api_complete:app --reload --port 8000
# Terminal 2:
pytest test_e2e.py -v --cov=api_complete
```

---

## 📊 EJERCICIO 5: Observabilidad Mínima Viable

**Directorio:** `semana7_ia/ejercicio5/`

**Objetivo:** Logging estructurado, métricas y dashboard para monitoreo en producción.

### Archivos Entregables

| Archivo | Líneas | Descripción |
|---------|--------|-------------|
| `api_observable.py` | 650 | API con logging JSON + métricas + traces |
| `dashboard_live.py` | 150 | Dashboard CLI en tiempo real |
| `DASHBOARD.md` | 580 | 5 gráficos esenciales + 3 alertas |
| `EJEMPLOS_LOGS.md` | 500 | Logs reales + queries jq + retention |
| `CRITICA_Y_MEJORA.md` | 800 | Análisis técnico + Prometheus/Grafana |
| `README.md` | 820 | Documentación completa |

**Total:** 6 archivos, ~3,500 líneas

### Features Destacadas
- ✅ Logging estructurado JSON (ts, correlationId, latency_ms)
- ✅ Métricas: P50/P95/P99 latency, error_rate_4xx_5xx
- ✅ Request tracing (pipeline completo con timestamps)
- ✅ Dashboard CLI con auto-refresh (5s)
- ✅ 3 alertas: High 5xx (>1%), High Latency (P95 >50ms), High 4xx POST (>15%)

### Quickstart
```bash
cd semana7_ia/ejercicio5
# Terminal 1:
uvicorn api_observable:app --reload --port 8000
# Terminal 2:
python dashboard_live.py
# Terminal 3:
curl http://localhost:8000/api/v1/_metrics | jq
```

---

## 📚 RECURSOS COMPARTIDOS

### Stack Tecnológico
- **Framework:** FastAPI 0.104+
- **Validation:** Pydantic 2.5+
- **Testing:** pytest + httpx
- **Database:** In-memory (Dict-based, con asyncio.Lock)
- **Auth:** JWT (HS256) con python-jose
- **Observability:** Logging estructurado JSON

### Patrones Implementados
- ✅ DTO Pattern (Data Transfer Objects)
- ✅ Middleware Pattern (autenticación, rate limiting, observability)
- ✅ Repository Pattern (InMemoryDB)
- ✅ Optimistic Locking (version field)
- ✅ Fixtures Pattern (pytest con autouse)
- ✅ Structured Logging (JSON con correlationId)

### Comandos Útiles

```bash
# Ver estructura completa
tree /F semana7_ia

# Instalar dependencias para todos los ejercicios
pip install fastapi uvicorn pydantic pytest httpx python-jose python-multipart requests

# Ejecutar todos los tests
cd semana7_ia
pytest ejercicio1/test_api.py -v
pytest ejercicio2/test_security.py -v
python ejercicio3/fuzzing_tests.py
pytest ejercicio4/test_e2e.py -v --cov=ejercicio4/api_complete

# Ver logs estructurados (ejercicio 5)
cd ejercicio5
uvicorn api_observable:app --reload --port 8000 2>&1 | grep -E "correlationId|latency_ms"
```

---

## 🎓 LECCIONES APRENDIDAS

### Fortalezas de la IA
1. **Scaffolding rápido:** Genera estructura completa en minutos
2. **Best practices:** Implementa patrones sin configuración manual
3. **Documentación:** README, críticas, prompts mejorados automáticos
4. **Tests comprehensivos:** 48 casos sin escribir código manual

### Limitaciones Encontradas
1. **Base de datos:** In-memory (no persiste, no constraints SQL)
2. **Autenticación:** No integrada entre ejercicios 2 y 4/5
3. **Métricas:** En memoria (no Prometheus)
4. **Logs:** stdout (no RotatingFileHandler)
5. **Alertas:** CLI (no webhooks Slack/PagerDuty)

### Mejoras para Producción
- [ ] Migrar a PostgreSQL con SQLAlchemy
- [ ] Integrar JWT de Ejercicio 2 en Ejercicios 4/5
- [ ] Implementar Prometheus + Grafana
- [ ] OpenTelemetry para distributed tracing
- [ ] Log rotation con RotatingFileHandler
- [ ] Alertas con webhooks (Slack, PagerDuty)
- [ ] CI/CD con GitHub Actions

---

## 🎯 MATRIZ DE COBERTURA

| Ejercicio | Endpoints | Tests | Coverage | Logs | Metrics | Docs |
|-----------|-----------|-------|----------|------|---------|------|
| **Ejercicio 1** | 6 | 18 | 100% | ❌ | ❌ | ✅ |
| **Ejercicio 2** | 8 | 6 | 85% | ✅ | ❌ | ✅ |
| **Ejercicio 3** | N/A | 10 | N/A | ❌ | ❌ | ✅ |
| **Ejercicio 4** | 7 | 48 | 95.6% | ❌ | ✅ | ✅ |
| **Ejercicio 5** | 9 | N/A | N/A | ✅ | ✅ | ✅ |

**Leyenda:**
- ✅ Implementado completamente
- ❌ No implementado (fuera de alcance del ejercicio)

---

## 📝 FORMATO DE ENTREGA

Cada ejercicio incluye:

1. **Prompt inicial** (en HTML de actividades)
2. **Respuesta de IA** (código generado)
3. **Crítica técnica** (`CRITICA_Y_MEJORA.md`)
   - Fortalezas (5-7 puntos)
   - Debilidades (5-7 puntos)
   - Prompt mejorado v2 (production-grade)
4. **Evidencia** (código funcional + tests + screenshots)
5. **README** (quickstart, troubleshooting, referencias)

---

## 🚀 PRÓXIMOS PASOS

### Integración de Ejercicios
1. Combinar Ejercicio 2 (JWT) + Ejercicio 4 (E2E tests) → Tests de autenticación
2. Combinar Ejercicio 2 (JWT) + Ejercicio 5 (Observability) → Logs con userId real
3. Combinar Ejercicio 4 (E2E) + Ejercicio 5 (Observability) → Tests de métricas

### Ejercicios Adicionales (Opcionales)
- **Ejercicio 6:** GraphQL API con Apollo Server
- **Ejercicio 7:** WebSockets para notificaciones real-time
- **Ejercicio 8:** Background jobs con Celery + Redis
- **Ejercicio 9:** API Gateway con rate limiting global
- **Ejercicio 10:** Deployment a Kubernetes con Helm

---

## 📞 CONTACTO Y REFERENCIAS

**Autor:** Semana 7 IA - Programación del Lado del Servidor  
**Fecha:** 26 Nov 2025  
**Versión:** 1.0.0

**Referencias:**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic V2 Docs](https://docs.pydantic.dev/latest/)
- [Google SRE Book](https://sre.google/sre-book/)
- [OpenAPI 3.0 Spec](https://swagger.io/specification/)
- [JSON Schema Draft-07](https://json-schema.org/draft-07/schema)

---

**✅ TODOS LOS EJERCICIOS COMPLETADOS CON ÉXITO** 🎉
