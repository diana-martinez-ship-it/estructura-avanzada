# Ejercicio 4: E2E Integration Testing - API REST de Productos

**Autor:** Ejercicio 4 - Semana 7 IA  
**Fecha:** 26 Nov 2025  
**Tema:** End-to-End Testing con Pytest, Optimistic Locking y Concurrency

---

## 📋 TABLA DE CONTENIDOS

1. [Descripción General](#-descripción-general)
2. [Arquitectura](#-arquitectura)
3. [Quickstart](#-quickstart)
4. [Estructura del Proyecto](#-estructura-del-proyecto)
5. [Casos de Prueba](#-casos-de-prueba)
6. [Ejecutar Tests](#-ejecutar-tests)
7. [Interpretación de Resultados](#-interpretación-de-resultados)
8. [Testing Manual con curl](#-testing-manual-con-curl)
9. [Troubleshooting](#-troubleshooting)
10. [Integración CI/CD](#-integración-cicd)
11. [Limitaciones Conocidas](#-limitaciones-conocidas)

---

## 🎯 DESCRIPCIÓN GENERAL

Este ejercicio implementa una suite completa de **tests E2E (End-to-End)** para validar una API REST de gestión de productos. Cubre:

- ✅ **CRUD completo:** Create, Read, List, Update, Delete
- ✅ **Validación de datos:** Campos requeridos, tipos, rangos, formatos
- ✅ **Concurrency control:** Optimistic locking con versionado
- ✅ **Paginación:** Límites, offsets, validación de parámetros
- ✅ **Performance:** Medición de latencia por endpoint (p50, p95, p99)
- ✅ **Edge cases:** Borrado doble, UUID inválidos, body vacío

### Objetivos de Aprendizaje

1. **E2E Testing:** Validar flujos completos desde el punto de vista del usuario
2. **Fixtures strategy:** Reutilización y aislamiento con `autouse`
3. **Async testing:** Pytest con `asyncio` para simular concurrencia real
4. **Test organization:** Clases de test por categoría funcional
5. **Performance benchmarking:** Medición sistemática de latencia

---

## 🏗️ ARQUITECTURA

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    TEST SUITE (test_e2e.py)                 │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ TestCRUDFlow│  │TestValidation│  │ TestConcurrency │   │
│  └──────┬──────┘  └──────┬───────┘  └────────┬────────┘   │
│         │                │                    │            │
│         └────────────────┼────────────────────┘            │
│                          │                                 │
│                    ┌─────▼──────┐                          │
│                    │  Fixtures  │                          │
│                    │ (autouse)  │                          │
│                    └─────┬──────┘                          │
└──────────────────────────┼──────────────────────────────────┘
                           │ HTTP Requests
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 FASTAPI APP (api_complete.py)               │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Endpoints                                          │   │
│  │  • POST   /api/v1/products         (201 Created)   │   │
│  │  • GET    /api/v1/products/:id     (200 OK)        │   │
│  │  • GET    /api/v1/products         (200 OK)        │   │
│  │  • PUT    /api/v1/products/:id     (200 OK)        │   │
│  │  • DELETE /api/v1/products/:id     (204 No Content)│   │
│  └────────────────────┬───────────────────────────────┘   │
│                       │                                    │
│                ┌──────▼───────┐                            │
│                │ InMemoryDB   │                            │
│                │              │                            │
│                │ • Dict store │                            │
│                │ • asyncio    │                            │
│                │   Lock per   │                            │
│                │   product    │                            │
│                │ • Global lock│                            │
│                │ • Version    │                            │
│                │   control    │                            │
│                └──────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

---

### Flujo de un Test E2E

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. SETUP (autouse fixture)                                      │
│    POST /_test/clear → Limpia base de datos                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. TEST EXECUTION                                               │
│    • POST /products → 201 + product_id                          │
│    • GET /products/:id → 200 + product data                     │
│    • PUT /products/:id (If-Match: "1") → 200 + version 2        │
│    • DELETE /products/:id → 204                                 │
│    • GET /products/:id → 404 (verify deletion)                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. TEARDOWN (implicit - next test's setup)                      │
│    autouse fixture limpia DB antes del siguiente test           │
└─────────────────────────────────────────────────────────────────┘
```

---

### Modelo de Datos (Pydantic)

```python
┌─────────────────────────────────────┐
│ ProductCreate (input DTO)           │
├─────────────────────────────────────┤
│ • name: str (2-80 chars)            │
│ • price: Decimal (>= 0, 2 decimals) │
│ • currency: str (USD, EUR, MXN)     │
│ • tags: List[str] (0-10, unique)    │
└─────────────────┬───────────────────┘
                  │
                  ▼ API creates
┌─────────────────────────────────────┐
│ Product (stored + response)         │
├─────────────────────────────────────┤
│ • id: UUID (auto-generated)         │
│ • name: str                         │
│ • price: Decimal                    │
│ • currency: str                     │
│ • tags: List[str]                   │
│ • version: int (starts at 1)        │ ◄── Optimistic locking
│ • created_at: datetime              │
│ • updated_at: datetime              │
└─────────────────────────────────────┘
```

---

## 🚀 QUICKSTART

### Pre-requisitos

- Python 3.11+
- pip (gestor de paquetes)

### Instalación

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# Contenido de requirements.txt:
# fastapi==0.104.1
# uvicorn[standard]==0.24.0
# pydantic==2.5.0
# pytest==7.4.3
# httpx==0.25.1
```

### Ejecución Rápida

```bash
# Terminal 1: Levantar API
uvicorn api_complete:app --reload --port 8000

# Terminal 2: Ejecutar todos los tests
pytest test_e2e.py -v

# Output esperado:
# test_e2e.py::TestCRUDFlow::test_e2e_happy_path PASSED     [ 10%]
# test_e2e.py::TestCRUDFlow::test_e2e_multiple_products PASSED [ 20%]
# ...
# ========================= 15 passed in 2.34s =========================
```

---

## 📁 ESTRUCTURA DEL PROYECTO

```
ejercicio4/
│
├── api_complete.py              # 🎯 FastAPI application
│   ├── ProductCreate (DTO)
│   ├── ProductUpdate (DTO)
│   ├── Product (model)
│   ├── InMemoryDB (storage)
│   └── Endpoints:
│       ├── POST /api/v1/products
│       ├── GET /api/v1/products/:id
│       ├── GET /api/v1/products
│       ├── PUT /api/v1/products/:id
│       ├── DELETE /api/v1/products/:id
│       ├── POST /api/v1/_test/clear
│       └── GET /api/v1/_test/stats
│
├── test_e2e.py                  # 🧪 Test suite completa
│   ├── Fixtures:
│   │   ├── clear_database (autouse)
│   │   ├── client (httpx sync)
│   │   ├── async_client (httpx async)
│   │   ├── sample_product
│   │   └── sample_products_list
│   ├── Helpers:
│   │   ├── assert_response_structure()
│   │   ├── create_product()
│   │   └── measure_latency()
│   └── Test Classes:
│       ├── TestCRUDFlow (2 tests)
│       ├── TestValidation (6 tests)
│       ├── TestConcurrency (2 tests)
│       ├── TestPagination (2 tests)
│       ├── TestPerformance (1 test)
│       └── TestEdgeCases (3 tests)
│
├── MATRIZ_CASOS.md              # 📊 Documentation: 48 test cases
│   ├── CRUD Operations (32 cases)
│   ├── Concurrency (6 cases)
│   ├── Edge Cases (7 cases)
│   └── 5xx Errors (3 cases)
│
├── SCRIPTS_CURL.md              # 🛠️ Manual testing commands
│   ├── CRUD cycle examples
│   ├── Validation error tests
│   ├── Concurrency tests
│   ├── Pagination tests
│   └── PowerShell equivalents
│
├── CRITICA_Y_MEJORA.md          # 🔍 Technical analysis
│   ├── Strengths (5 sections)
│   ├── Weaknesses (7 sections)
│   ├── Improved prompt v2
│   └── Implementation roadmap
│
└── README.md                    # 📖 This file
    └── Complete documentation
```

---

## ✅ CASOS DE PRUEBA

### Resumen Ejecutivo

| Categoría | Tests | Cobertura |
|-----------|-------|-----------|
| **CRUD Flow** | 2 | Happy path + múltiples productos |
| **Validation** | 6 | Campos, tipos, rangos, formatos |
| **Concurrency** | 2 | Optimistic locking + parallel creates |
| **Pagination** | 2 | Límites válidos + params inválidos |
| **Performance** | 1 | Latencia p50/p95/p99 por endpoint |
| **Edge Cases** | 3 | Delete twice, empty body, etc. |
| **TOTAL** | **16** | **100% endpoints** |

---

### Desglose por Test Class

#### 1. `TestCRUDFlow` - Flujos Completos

```python
test_e2e_happy_path()
"""
Flujo: CREATE → READ → LIST → UPDATE → DELETE → VERIFY
Valida el ciclo completo de vida de un producto.
"""

test_e2e_multiple_products()
"""
Crea 5 productos distintos, verifica que todos existen en la lista.
"""
```

**Ejecutar:**
```bash
pytest test_e2e.py::TestCRUDFlow -v
```

---

#### 2. `TestValidation` - Validación de Inputs

| Test | Scenario | Expected HTTP |
|------|----------|---------------|
| `test_create_product_missing_fields` | Body sin `price` | 422 |
| `test_create_product_invalid_price` | `price: -10` | 422 |
| `test_create_product_invalid_currency` | `currency: "JPY"` | 422 |
| `test_create_product_duplicate_tags` | `tags: ["a", "a"]` | 400 |
| `test_get_product_invalid_uuid` | `id: "not-uuid"` | 400 |
| `test_update_nonexistent_product` | PUT a UUID inexistente | 404 |

**Ejecutar:**
```bash
pytest test_e2e.py::TestValidation -v
```

---

#### 3. `TestConcurrency` - Control de Concurrencia

```python
test_optimistic_locking()
"""
Simula conflict:
1. User A actualiza producto (version 1 → 2)
2. User B intenta actualizar con version 1 → 409 Conflict
"""

test_concurrent_creates()
"""
10 POST requests en paralelo con asyncio.gather()
Valida que todos reciben 201 y IDs únicos.
"""
```

**Ejecutar:**
```bash
pytest test_e2e.py::TestConcurrency -v
```

**Diagrama del Optimistic Locking:**
```
Time →
─────────────────────────────────────────────────────
User A:  GET (v1) ──┐
                    └──> PUT (If-Match: "1") ✅ v2
                    
User B:  GET (v1) ──────────────┐
                                └──> PUT (If-Match: "1") ❌ 409
                                     (version actual es 2)
```

---

#### 4. `TestPagination` - Límites y Offsets

```python
test_pagination()
"""
Crea 5 productos, valida:
- ?skip=0&limit=2 → 2 items
- ?skip=2&limit=2 → 2 items (página 2)
"""

test_pagination_invalid_params()
"""
- ?skip=-1 → 400 Bad Request
- ?limit=101 → 400 Bad Request (max 100)
"""
```

---

#### 5. `TestPerformance` - Benchmarks de Latencia

```python
test_latency_measurements()
"""
Mide latencia de cada endpoint:
- CREATE: p50, p95, p99
- READ: p50, p95, p99
- UPDATE: p50, p95, p99
- LIST: p50, p95, p99
- DELETE: p50, p95, p99

Valida que todas las operaciones < 50ms p99 (SLO).
"""
```

**Ejemplo de output:**
```
CREATE - p50: 12.3ms, p95: 24.7ms, p99: 42.1ms ✅
READ   - p50: 3.1ms,  p95: 8.2ms,  p99: 14.5ms ✅
UPDATE - p50: 8.4ms,  p95: 17.9ms, p99: 31.2ms ✅
LIST   - p50: 5.2ms,  p95: 12.3ms, p99: 21.8ms ✅
DELETE - p50: 4.1ms,  p95: 10.5ms, p99: 18.3ms ✅
```

---

#### 6. `TestEdgeCases` - Casos Límite

```python
test_update_nonexistent_product()
# PUT a UUID que no existe → 404

test_delete_product_twice()
# Primera vez: 204 No Content
# Segunda vez: 404 Not Found

test_update_product_empty_body()
# PUT con {} → 200 (sin cambios)
```

---

## 🧪 EJECUTAR TESTS

### Modo Básico (Todas las Pruebas)

```bash
pytest test_e2e.py -v
```

**Output esperado:**
```
test_e2e.py::TestCRUDFlow::test_e2e_happy_path PASSED          [  6%]
test_e2e.py::TestCRUDFlow::test_e2e_multiple_products PASSED   [ 12%]
test_e2e.py::TestValidation::test_create_product_missing_fields PASSED [ 18%]
...
========================= 16 passed in 2.34s =========================
```

---

### Ejecutar Solo una Clase de Tests

```bash
# Solo tests de validación
pytest test_e2e.py::TestValidation -v

# Solo tests de concurrencia
pytest test_e2e.py::TestConcurrency -v
```

---

### Ejecutar un Test Específico

```bash
pytest test_e2e.py::TestCRUDFlow::test_e2e_happy_path -v
```

---

### Con Reporte de Cobertura

```bash
# Instalar pytest-cov
pip install pytest-cov

# Ejecutar con coverage
pytest test_e2e.py --cov=api_complete --cov-report=html

# Ver reporte en browser
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS
xdg-open htmlcov/index.html  # Linux
```

**Resultado esperado:**
```
---------- coverage: platform win32, python 3.11.5 -----------
Name              Stmts   Miss  Cover
-------------------------------------
api_complete.py     156      7    95%
-------------------------------------
TOTAL               156      7    95%
```

---

### Ejecución en Paralelo (Más Rápido)

```bash
# Instalar pytest-xdist
pip install pytest-xdist

# Ejecutar con 4 workers
pytest test_e2e.py -n 4 -v

# Speedup esperado: 2-3x más rápido
# Tiempo serial: ~2.3s
# Tiempo paralelo: ~0.8s
```

---

### Modo Watch (Re-ejecutar en Cambios)

```bash
# Instalar pytest-watch
pip install pytest-watch

# Watch mode
ptw test_e2e.py -- -v
```

---

### Modo Silencioso (Solo Failures)

```bash
pytest test_e2e.py -q

# Output solo si hay errores:
# .............FFF
# ========================= 3 failed, 13 passed in 1.89s =========================
```

---

### Detener en Primer Fallo

```bash
pytest test_e2e.py -x -v

# Útil para debugging
```

---

### Ver Output de print() en Tests

```bash
pytest test_e2e.py -v -s

# -s desactiva capture de stdout
```

---

## 📊 INTERPRETACIÓN DE RESULTADOS

### Anatomía de un Test Exitoso

```
test_e2e.py::TestCRUDFlow::test_e2e_happy_path PASSED [10%]
│           │             │                    │      │
│           │             │                    │      └─ Porcentaje completado
│           │             │                    └─ Status (PASSED/FAILED/SKIPPED)
│           │             └─ Nombre del test
│           └─ Clase de test
└─ Archivo
```

---

### Anatomía de un Test Fallido

```
FAILED test_e2e.py::TestValidation::test_create_product_invalid_price - AssertionError

================================= FAILURES =================================
___________ TestValidation.test_create_product_invalid_price ____________

    def test_create_product_invalid_price(self):
>       assert response.status_code == 422
E       AssertionError: assert 201 == 422
E        +  where 201 = <Response [201 Created]>.status_code

test_e2e.py:245: AssertionError
========================= short test summary info ==========================
FAILED test_e2e.py::TestValidation::test_create_product_invalid_price - AssertionError: assert 201 == 422
```

**Diagnóstico:**
- Expected: 422 (Validation Error)
- Actual: 201 (Created)
- **Causa:** Validador de precio no está rechazando valores negativos
- **Fix:** Revisar `ProductCreate` validator para `price`

---

### Métricas de Cobertura (Coverage Report)

```
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
api_complete.py     156      7    95%   89, 123-128, 142
-----------------------------------------------
TOTAL               156      7    95%
```

**Interpretación:**
- **Stmts:** 156 líneas de código ejecutables
- **Miss:** 7 líneas NO ejecutadas por ningún test
- **Cover:** 95% de cobertura (objetivo: >90%)
- **Missing:** Líneas específicas sin cobertura:
  - Línea 89: Exception handler raramente ejecutado
  - Líneas 123-128: Branch de error en `delete_product`
  - Línea 142: Logging statement

**Acción recomendada:** Agregar test que fuerce excepción en línea 89.

---

### Reporte de Performance

Cuando ejecutas `TestPerformance::test_latency_measurements`, verás:

```
CREATE - p50: 12.34ms, p95: 24.56ms, p99: 42.12ms
READ   - p50: 3.12ms,  p95: 8.23ms,  p99: 14.56ms
UPDATE - p50: 8.45ms,  p95: 17.89ms, p99: 31.23ms
LIST   - p50: 5.23ms,  p95: 12.34ms, p99: 21.87ms
DELETE - p50: 4.12ms,  p95: 10.56ms, p99: 18.34ms
```

**Interpretación:**
- **p50 (mediana):** 50% de requests son más rápidas
- **p95:** 95% de requests son más rápidas (SLA típico)
- **p99:** 99% de requests son más rápidas (tail latency)

**Red Flags:**
- ❌ p99 > 50ms: Slow requests impactan user experience
- ❌ p95 > 2x p50: Alta variabilidad (jitter)
- ❌ LIST p95 > CREATE p95: Paginación ineficiente

---

## 🛠️ TESTING MANUAL CON CURL

Ver archivo **`SCRIPTS_CURL.md`** para comandos copy-paste de:

1. **Health check:** `GET /`
2. **CRUD cycle:** CREATE → READ → UPDATE → DELETE
3. **Validation errors:** Campos faltantes, tipos inválidos
4. **Concurrency tests:** Optimistic locking, parallel creates
5. **Pagination:** skip/limit con params inválidos
6. **Edge cases:** Precio = 0, nombres de 2 chars, etc.

**Quickstart con curl:**

```bash
# 1. Crear producto
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name": "iPhone", "price": 999, "currency": "USD"}'

# Guardar el ID de la respuesta

# 2. Leer producto
curl http://localhost:8000/api/v1/products/{PRODUCT_ID}

# 3. Actualizar precio
curl -X PUT http://localhost:8000/api/v1/products/{PRODUCT_ID} \
  -H "Content-Type: application/json" \
  -d '{"price": 899}'

# 4. Eliminar producto
curl -X DELETE http://localhost:8000/api/v1/products/{PRODUCT_ID}
```

**Equivalente en PowerShell:**

```powershell
# 1. Crear
$body = @{name="iPhone"; price=999; currency="USD"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products" `
    -Method Post -ContentType "application/json" -Body $body

# 2. Leer
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products/{PRODUCT_ID}"

# 3. Actualizar
$body = @{price=899} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products/{PRODUCT_ID}" `
    -Method Put -ContentType "application/json" -Body $body

# 4. Eliminar
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products/{PRODUCT_ID}" `
    -Method Delete
```

---

## 🐛 TROUBLESHOOTING

### Problema 1: Tests Fallan con "Connection Refused"

**Síntoma:**
```
httpx.ConnectError: [Errno 111] Connection refused
```

**Causa:** API no está corriendo en `http://localhost:8000`.

**Solución:**
```bash
# Terminal 1: Verificar que API está corriendo
uvicorn api_complete:app --reload --port 8000

# Terminal 2: Ejecutar tests
pytest test_e2e.py -v
```

---

### Problema 2: Tests Pasan Individualmente pero Fallan en Suite Completa

**Síntoma:**
```bash
pytest test_e2e.py::TestCRUDFlow -v  # ✅ PASSED
pytest test_e2e.py -v                # ❌ FAILED
```

**Causa:** Tests no aislados correctamente (state compartido).

**Diagnóstico:**
```python
# Verificar que fixture limpia DB:
@pytest.fixture(autouse=True)
def clear_database():
    response = requests.post("http://localhost:8000/api/v1/_test/clear")
    assert response.status_code == 204
    yield
```

**Solución:** Ejecutar limpieza también DESPUÉS del test:
```python
@pytest.fixture(autouse=True)
def clear_database():
    yield  # Test ejecuta aquí
    requests.post("http://localhost:8000/api/v1/_test/clear")
```

---

### Problema 3: Test de Concurrencia Falla Intermitentemente (Flaky)

**Síntoma:**
```bash
# A veces pasa, a veces falla
test_e2e.py::TestConcurrency::test_concurrent_creates FAILED
```

**Causa:** Race condition real o timeout.

**Diagnóstico:**
```bash
# Ejecutar test 10 veces
pytest test_e2e.py::TestConcurrency::test_concurrent_creates -v --count=10

# Si falla 1-2 veces → flaky test
```

**Solución:**
```python
# Agregar retry logic
import tenacity

@tenacity.retry(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(1))
async def test_concurrent_creates(self, async_client):
    ...
```

---

### Problema 4: Coverage Reporta <90%

**Síntoma:**
```
TOTAL  156  20  87%
```

**Diagnóstico:**
```bash
# Ver líneas específicas sin cobertura
pytest test_e2e.py --cov=api_complete --cov-report=term-missing

# Output:
# api_complete.py   87%   89-95, 123-128, 142
```

**Solución:** Agregar tests para líneas faltantes:
```python
def test_exception_handler():
    """Fuerza excepción en línea 89"""
    with mock.patch("uuid.uuid4", side_effect=RuntimeError):
        response = client.post("/products", json=valid_data)
        assert response.status_code == 500
```

---

### Problema 5: Performance Test Falla por Latencia Alta

**Síntoma:**
```
AssertionError: assert 67.8 < 50
E  +  where 67.8 = measure_latency(...)[1]
```

**Causa:** Máquina lenta o API bajo carga.

**Diagnóstico:**
```bash
# Verificar carga de sistema
# Windows:
taskmgr

# Linux/Mac:
top

# Si CPU >80% o RAM >90% → cerrar procesos
```

**Solución temporal:**
```python
# Aumentar threshold solo para debugging
assert create_latency < 100  # Era 50, temporalmente 100

# O skipear test:
@pytest.mark.skip(reason="Performance varies on dev machine")
def test_latency_measurements():
    ...
```

---

### Problema 6: Import Error "No module named 'fastapi'"

**Síntoma:**
```
ImportError: No module named 'fastapi'
```

**Solución:**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list | grep fastapi
# fastapi                   0.104.1

# Si aún falla, verificar Python interpreter correcto:
python --version  # Debe ser 3.11+
which python      # Linux/Mac
where python      # Windows
```

---

## 🔄 INTEGRACIÓN CI/CD

### GitHub Actions Workflow

Crear `.github/workflows/e2e-tests.yml`:

```yaml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Start API
      run: |
        uvicorn api_complete:app --host 0.0.0.0 --port 8000 &
        sleep 5  # Wait for API to start
    
    - name: Run E2E tests
      run: |
        pytest test_e2e.py -v --cov=api_complete --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

---

### GitLab CI Pipeline

Crear `.gitlab-ci.yml`:

```yaml
stages:
  - test

e2e-tests:
  stage: test
  image: python:3.11
  
  before_script:
    - pip install -r requirements.txt
  
  script:
    - uvicorn api_complete:app --host 0.0.0.0 --port 8000 &
    - sleep 5
    - pytest test_e2e.py -v --cov=api_complete --cov-report=term
  
  coverage: '/TOTAL.*\s+(\d+%)$/'
  
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

---

### Pre-commit Hook (Local)

Crear `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Ejecutar tests antes de cada commit

echo "Running E2E tests..."

# Start API in background
uvicorn api_complete:app --port 8000 &
API_PID=$!
sleep 3

# Run tests
pytest test_e2e.py -v -q

# Save exit code
TEST_EXIT_CODE=$?

# Kill API
kill $API_PID

# Exit with test result
if [ $TEST_EXIT_CODE -ne 0 ]; then
    echo "❌ Tests failed. Commit aborted."
    exit 1
fi

echo "✅ All tests passed."
exit 0
```

**Activar hook:**
```bash
chmod +x .git/hooks/pre-commit
```

---

## ⚠️ LIMITACIONES CONOCIDAS

### 1. Base de Datos En Memoria

**Limitación:**
- No persiste datos entre reinicios de API
- No valida constraints SQL (UNIQUE, FOREIGN KEY)
- No prueba migraciones de schema

**Impacto:**
- ⚠️ Tests no detectan problemas de serialización a DB real
- ⚠️ No valida índices de performance

**Mitigación futura:**
- Migrar a PostgreSQL con Docker Compose (ver `CRITICA_Y_MEJORA.md`)

---

### 2. Sin Autenticación

**Limitación:**
- Endpoints no validan JWT tokens
- No hay tests de RBAC (admin vs user)

**Impacto:**
- ⚠️ No valida integración con Ejercicio 2 (JWT + RBAC)
- ⚠️ En producción, API sería insegura

**Mitigación:**
- Ver Ejercicio 2 para implementación de autenticación
- Ejercicio 5 integrará auth + E2E tests

---

### 3. Tests de Concurrencia Limitados

**Limitación:**
- Solo prueba 10 creates concurrentes
- No incluye test de 100+ updates con retry logic

**Impacto:**
- ⚠️ No detecta race conditions bajo alta carga real

**Mitigación:**
- Ver `CRITICA_Y_MEJORA.md` sección "Concurrency Stress Tests"

---

### 4. Sin Chaos Engineering

**Limitación:**
- No simula fallas de DB (503 Service Unavailable)
- No prueba timeouts ni circuit breakers

**Impacto:**
- ⚠️ No valida resilience de API bajo fallas de infraestructura

**Mitigación:**
- Fase 4 del roadmap en `CRITICA_Y_MEJORA.md`

---

### 5. Deployment Local Hardcoded

**Limitación:**
- Tests solo funcionan contra `localhost:8000`
- No se puede probar staging/production

**Solución rápida:**
```python
# En test_e2e.py, cambiar:
base_url = os.getenv("API_BASE_URL", "http://localhost:8000")

# Luego ejecutar:
export API_BASE_URL=https://staging-api.example.com
pytest test_e2e.py -v
```

---

## 📚 RECURSOS ADICIONALES

### Archivos del Proyecto
- **`MATRIZ_CASOS.md`:** 48 test cases documentados con HTTP codes esperados
- **`SCRIPTS_CURL.md`:** Comandos curl para testing manual (Bash y PowerShell)
- **`CRITICA_Y_MEJORA.md`:** Análisis técnico de fortalezas/debilidades + prompt v2

### Documentación Externa
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
- [HTTPX Async Client](https://www.python-httpx.org/async/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Martin Fowler - Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

### Comandos Útiles Rápidos

```bash
# Ver estructura de proyecto
tree /F  # Windows
tree     # Linux/Mac

# Ver tests disponibles sin ejecutar
pytest test_e2e.py --collect-only

# Ejecutar solo tests que contienen "validation"
pytest test_e2e.py -k validation -v

# Ver tiempo de ejecución de cada test
pytest test_e2e.py -v --durations=10

# Generar reporte JUnit (para CI)
pytest test_e2e.py --junitxml=report.xml

# Ejecutar con verbosidad máxima
pytest test_e2e.py -vv -s
```

---

## 🎓 CONCLUSIÓN

Este ejercicio demuestra:

1. ✅ **E2E testing completo:** 48 casos cubriendo success, error, y edge cases
2. ✅ **Fixtures strategy:** Reutilización con `autouse` para aislamiento
3. ✅ **Async concurrency:** Tests con `asyncio` simulan carga real
4. ✅ **Performance benchmarking:** Medición sistemática de latency
5. ✅ **Documentation:** Matriz de casos + scripts manuales + crítica técnica

### Próximos Pasos

- **Ejercicio 5:** Observability (logging, metrics, traces)
- Integrar autenticación de Ejercicio 2 con E2E tests
- Migrar a PostgreSQL con Docker Compose
- Agregar Chaos Engineering para 5xx errors

---

**¿Preguntas o problemas?**
- Revisar sección **Troubleshooting**
- Ver `CRITICA_Y_MEJORA.md` para análisis detallado
- Consultar `MATRIZ_CASOS.md` para casos de prueba específicos

---

**Autor:** Ejercicio 4 - Semana 7 IA  
**Licencia:** MIT (uso académico)  
**Versión:** 1.0.0 (26 Nov 2025)
