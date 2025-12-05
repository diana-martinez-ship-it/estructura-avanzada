# Crítica Técnica - Ejercicio 3: Validación y Serialización Determinista

---

## 📊 Evaluación de la Implementación

### ✅ **FORTALEZAS**

#### 1. **JSON Schema Completo y Reutilizable**
```json
"$ref": "#/definitions/Product/properties/name"
```

**Por qué es bueno:**
- Schema centralizado → cambios en un solo lugar
- Reutilización con `$ref` → DRY principle
- Documentación auto-generada → OpenAPI, docs web
- Validación en frontend y backend con mismo schema

**Beneficios:**
✅ Consistencia entre capas (frontend valida igual que backend)  
✅ Menos código duplicado  
✅ Más fácil mantener (cambias regex en un lugar)

---

#### 2. **additionalProperties: false**
```json
{
  "additionalProperties": false
}
```

**Por qué es bueno:**
- Rechaza campos no definidos → previene data leaks
- Fuerza contrato estricto → API predecible
- Protege contra mass assignment vulnerabilities

**Ejemplo de ataque prevenido:**
```json
// Usuario envía:
{ "name": "Product", "price": 100, "isAdmin": true }
                                        ↑
// additionalProperties: false rechaza "isAdmin"
```

---

#### 3. **Serialización con Orden Determinista**
```python
PROPERTY_ORDER = ["id", "name", "price", "currency", "tags", "createdAt"]

def serialize(product):
    return {key: product[key] for key in PROPERTY_ORDER if key in product}
```

**Por qué es bueno:**
- JSON siempre igual → caching eficiente (ETags, HTTP cache)
- Testing predecible → snapshots no cambian aleatoriamente
- Debugging más fácil → siempre ves campos en mismo orden

**Problema que resuelve:**
```python
# Sin orden determinista:
{"price": 100, "name": "Product", "id": "123"}  # Request 1
{"id": "123", "price": 100, "name": "Product"}  # Request 2
# Mismo contenido, diferente representación → cache miss
```

---

#### 4. **Sanitización de Entrada**
```python
def _sanitize_string(value: str) -> str:
    sanitized = value.strip()
    sanitized = re.sub(r'\s+', ' ', sanitized)  # Colapsar espacios
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32)
    return sanitized
```

**Por qué es bueno:**
- Previene ataques con caracteres de control
- Normaliza entrada (espacios múltiples → uno)
- Elimina null bytes → previene truncation attacks

**Ataques prevenidos:**
- Null byte injection: `"Product\x00Admin"`
- Control character injection: `"Product\r\n<script>"`

---

#### 5. **Validación Granular con Mensajes Claros**
```json
{
  "field": "tags[2]",
  "issue": "Solo se permiten minúsculas y guiones (a-z0-9-)",
  "received": "SALE!"
}
```

**Por qué es bueno:**
- Frontend sabe exactamente qué campo arreglar
- `received` ayuda a debugging
- Índice en arrays (`tags[2]`) → precisión

**UX mejorado:**
```
❌ Malo: "Validation error"
✅ Bueno: "tags[2]: Solo se permiten minúsculas y guiones (a-z0-9-)"
```

---

#### 6. **Acumulación de Errores**
```python
errors = []
try:
    validated["name"] = validate_name(data["name"])
except ValidationError as e:
    errors.append(e)

# ... validar todos los campos

if errors:
    raise create_validation_exception(errors)
```

**Por qué es bueno:**
- Usuario ve TODOS los problemas de una vez
- Evita "whack-a-mole" debugging (arreglas uno, aparece otro)
- Menos round-trips al servidor

**Comparación:**
```
❌ Sin acumulación: 
  Request 1 → "name muy corto"
  Request 2 → "price negativo"  
  Request 3 → "currency inválida"
  = 3 requests

✅ Con acumulación:
  Request 1 → ["name muy corto", "price negativo", "currency inválida"]
  = 1 request
```

---

### ❌ **DEBILIDADES**

#### 1. **Validación de Regex No Tiene Timeout**
```python
❌ re.match(r"^[\p{L}\p{N}\s\-_.,()]+$", sanitized)
```

**Problema:**
- Regex complejos pueden causar ReDoS (Regular Expression Denial of Service)
- Atacante envía input que causa catastrophic backtracking

**Impacto:**
```python
# Input malicioso:
name = "A" * 100000  # 100k caracteres
# Regex tarda minutos/horas en rechazar
# → Bloquea thread del servidor
```

**Solución:**
```python
import re
import signal

def validate_with_timeout(pattern, text, timeout=1):
    def handler(signum, frame):
        raise TimeoutError("Regex timeout")
    
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    
    try:
        return re.match(pattern, text)
    finally:
        signal.alarm(0)
```

**Mejor solución:**
- Usar bibliotecas con límites: `re2` (Google's RE2 engine)
- Pre-validar longitud antes de regex

---

#### 2. **No Valida Longitud de Payload Total**
```python
❌ Sin límite de tamaño de request body
```

**Problema:**
- Atacante puede enviar payload de 1GB
- Consume memoria del servidor → DoS
- JSON parse de payloads grandes es lento

**Impacto:**
```python
# Payload malicioso:
{
  "name": "Product",
  "tags": ["tag1", "tag2", ..., "tag1000000"]  # 1 millón de tags
}
# Consume gigabytes de RAM al parsear
```

**Solución:**
```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

class PayloadSizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        
        if content_length:
            if int(content_length) > 1_000_000:  # 1MB
                return JSONResponse(
                    status_code=413,
                    content={"error": {"code": "PAYLOAD_TOO_LARGE", "msg": "Máximo 1MB"}}
                )
        
        return await call_next(request)
```

---

#### 3. **Sanitización No Escapa HTML/SQL**
```python
❌ Solo elimina caracteres de control, no escapa <>"'
```

**Problema:**
- Name con `<script>alert(1)</script>` pasa validación
- Si se renderiza en HTML sin escapar → XSS
- SQL queries sin prepared statements → SQLi

**Impacto:**
```python
# Entrada:
{"name": "<script>alert(document.cookie)</script>"}

# Se guarda en DB y luego se muestra en HTML:
<h1>Product: <script>alert(document.cookie)</script></h1>
# → XSS ejecuta en navegador del usuario
```

**Solución:**
```python
import html
import re

def sanitize_for_html(value: str) -> str:
    # Escapar HTML
    escaped = html.escape(value)
    # Eliminar tags HTML residuales
    escaped = re.sub(r'<[^>]+>', '', escaped)
    return escaped

def validate_name(value):
    # ... validaciones existentes
    sanitized = sanitize_for_html(sanitized)
    return sanitized
```

**Mejor práctica:**
- Sanitizar en entrada (como hacemos)
- Escapar en salida (template engine debe hacerlo)
- Usar prepared statements en DB

---

#### 4. **Tags No Valida Contenido Semántico**
```python
❌ Acepta tags vacíos de significado: "aaa", "xyz123"
```

**Problema:**
- No hay whitelist de tags permitidos
- Usuarios pueden crear tags basura
- Dificulta búsquedas y filtrado

**Impacto:**
```python
# Tags inútiles:
{"tags": ["aaa", "bbb", "ccc", "x", "y", "z"]}

# vs. Tags útiles:
{"tags": ["electronics", "laptops", "gaming"]}
```

**Solución:**
```python
# Opción 1: Whitelist de categorías
ALLOWED_CATEGORIES = {"electronics", "clothing", "food", "books", ...}

def validate_tags(tags):
    for tag in tags:
        if tag not in ALLOWED_CATEGORIES:
            raise ValidationError(f"Tag '{tag}' no está en categorías permitidas")

# Opción 2: Sugerencias (fuzzy matching)
from difflib import get_close_matches

def suggest_tag(user_tag):
    matches = get_close_matches(user_tag, ALLOWED_CATEGORIES, n=3)
    return matches  # ["electronics", "electric", "electron"]
```

---

#### 5. **Currency Limitado a 3 Monedas**
```python
❌ "enum": ["MXN", "USD", "EUR"]
```

**Problema:**
- No escalable si quieres expandir internacionalmente
- Hardcodeado en schema → cambios requieren deploy
- No soporta criptomonedas (BTC, ETH)

**Impacto:**
- Negocio expande a Asia → necesitas JPY, CNY, KRW
- Cada nueva moneda requiere cambio de código

**Solución:**
```python
# Opción 1: ISO 4217 completo (170+ monedas)
import pycountry

def validate_currency(code):
    try:
        currency = pycountry.currencies.get(alpha_3=code)
        return currency.alpha_3
    except:
        raise ValidationError(f"Código ISO 4217 inválido: {code}")

# Opción 2: Lista dinámica desde DB
async def get_supported_currencies():
    return await db.query("SELECT code FROM currencies WHERE active = true")
```

---

#### 6. **createdAt No Valida Rango Temporal**
```python
❌ Acepta fechas en el futuro o muy antiguas
```

**Problema:**
- `createdAt: "2099-01-01"` es técnicamente válido pero ilógico
- Fechas antes de 1970 pueden causar problemas (epoch negativo)

**Impacto:**
```python
# Usuario malicioso:
{"createdAt": "2999-12-31T23:59:59.999Z"}

# En queries de "últimos 30 días":
WHERE createdAt >= NOW() - INTERVAL '30 days'
# → Producto no aparece porque está "en el futuro"
```

**Solución:**
```python
from datetime import datetime, timezone, timedelta

def validate_created_at(value):
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    
    # No puede ser más de 1 minuto en el futuro (clock skew)
    if dt > now + timedelta(minutes=1):
        raise ValidationError("createdAt no puede estar en el futuro")
    
    # No puede ser antes de 2000-01-01
    if dt < datetime(2000, 1, 1, tzinfo=timezone.utc):
        raise ValidationError("createdAt demasiado antiguo")
    
    return value
```

---

#### 7. **No Hay Normalización de Unicode**
```python
❌ "Café" vs "Café" (diferentes representaciones Unicode)
```

**Problema:**
- Unicode permite múltiples formas de representar mismo texto
- `"Café"` puede ser:
  - `"Caf\u00e9"` (NFC - composed)
  - `"Cafe\u0301"` (NFD - decomposed)
- Duplicados en búsquedas y comparaciones

**Impacto:**
```python
# Usuario 1 crea:
{"name": "Café"}  # \u00e9

# Usuario 2 busca:
search("Café")  # \u0301
# → No encuentra, aunque es "el mismo" texto
```

**Solución:**
```python
import unicodedata

def normalize_string(value: str) -> str:
    # Normalizar a NFC (forma canónica compuesta)
    normalized = unicodedata.normalize('NFC', value)
    return normalized

def validate_name(value):
    sanitized = normalize_string(value)
    # ... resto de validaciones
```

---

#### 8. **Fuzzing No Cubre Casos Concurrentes**
```python
❌ Tests son secuenciales, no prueban race conditions
```

**Problema:**
- Validación puede tener bugs en concurrencia
- Dos requests simultáneos pueden causar estados inconsistentes

**Impacto:**
```python
# Thread 1 y Thread 2 validan simultáneamente:
# Ambos pasan validación
# Ambos escriben a DB
# → Duplicados en DB (violación de unicidad)
```

**Solución:**
```python
import threading
import time

def test_concurrent_validation():
    results = []
    
    def validate_concurrent():
        try:
            validated = ProductValidator.validate_create_request({
                "name": "Product",
                "price": 100,
                "currency": "USD"
            })
            results.append(("success", validated))
        except Exception as e:
            results.append(("error", str(e)))
    
    # 100 threads validando simultáneamente
    threads = [threading.Thread(target=validate_concurrent) for _ in range(100)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # Verificar que todos pasaron
    assert all(r[0] == "success" for r in results)
```

---

## 🎯 **PROMPT MEJORADO**

```
Actúa como especialista en datos y seguridad backend.

Define esquemas de validación para una API REST de productos con las siguientes características:

MODELO Product:
- id: UUID v4 (generado por servidor)
- name: string (2-100 chars, Unicode normalizado NFC, sanitizado HTML/SQL)
- price: decimal (>= 0, <= 1B, exactamente 2 decimales)
- currency: ISO 4217 (usar biblioteca pycountry, soportar 170+ monedas)
- tags: array 0-10 strings únicos (a-z0-9-, sugerencias fuzzy desde whitelist)
- createdAt: ISO-8601 UTC (validar rango: 2000-01-01 hasta now+1min)
- metadata: object opcional con validación recursiva (max depth=3)

REQUERIMIENTOS DE VALIDACIÓN:

1. JSON SCHEMA:
   - Draft-07 completo con $ref, allOf, oneOf
   - additionalProperties: false estricto
   - Patrones regex con alternativa re2 (no backtracking)
   - Ejemplos inline de valid/invalid

2. SANITIZACIÓN:
   - Unicode normalización (NFC)
   - HTML escape (<>"'&)
   - SQL escape (prevenir inyección)
   - Control characters removal (excepto \n\t)
   - Null byte protection

3. LÍMITES DE PAYLOAD:
   - Middleware de límite: 1MB total
   - Límite de profundidad de anidación: 5 niveles
   - Timeout de validación: 500ms por request
   - Rate limiting en endpoint de validación: 100 req/min por IP

4. SERIALIZACIÓN DETERMINISTA:
   - Orden fijo de propiedades (alfabético o custom)
   - Omitir valores null/undefined
   - Precisión de decimales fija (2 dígitos)
   - Timestamps siempre UTC con milisegundos

5. MANEJO DE ERRORES:
   - Código HTTP: 400 para validación, 413 para payload grande, 422 para lógica
   - Formato: { data: null, error: { code, msg, details: [{field, issue, received}] }, meta }
   - Acumular TODOS los errores en un solo response
   - Incluir sugerencias de corrección cuando sea posible

6. TABLA DE ERRORES:
   - 15 códigos específicos (MISSING_REQUIRED, INVALID_TYPE, OUT_OF_RANGE, etc.)
   - Para cada uno: descripción, ejemplo input, respuesta JSON, HTTP status
   - Estrategia de retry para cliente (reintentar o no)

7. FUZZING (20 CASOS):
   - SQL injection ('; DROP TABLE)
   - XSS (<script>, onerror=)
   - Unicode overflow (emoji, CJK, RTL)
   - ReDoS (regex catastrophic backtracking)
   - Float edge cases (Infinity, NaN, -0)
   - Null byte injection (\x00)
   - DoS payloads (arrays gigantes, strings de 1GB)
   - Type juggling (bool en number, null en string)
   - Deeply nested objects (10 niveles)
   - Concurrent validation (100 threads simultáneos)
   - Time-of-check-time-of-use (TOCTOU)
   - Locale-dependent bugs (. vs , en decimales)
   - Encoding attacks (UTF-7, UTF-16)
   - Hash collision attacks (tags con mismo hash)
   - Timing attacks (password comparison)

8. TESTING:
   - 30 tests unitarios (pytest)
   - 20 tests de fuzzing con property-based testing (hypothesis)
   - 10 tests de integración (boundary values)
   - 5 tests de performance (latencia < 50ms p95)
   - Coverage: 100% de líneas, 95% de branches

9. OBSERVABILIDAD:
   - Log estructurado de cada validación fallida
   - Métrica: validation_errors_total{field, error_code}
   - Métrica: validation_latency_seconds (histogram)
   - Alerta si error_rate > 10% en 5 minutos

10. DOCUMENTACIÓN:
    - README con quickstart y ejemplos
    - JSON Schema exportado a OpenAPI 3.1
    - Tabla markdown con todos los errores
    - Diagrama de flujo de validación (Mermaid)
    - Guía de mitigación de ataques

ENTREGABLES:
1) schemas.json (JSON Schema Draft-07 completo)
2) validators.py (código Python con validators)
3) TABLA_ERRORES.md (15 errores documentados)
4) fuzzing_tests.py (20 casos de fuzzing)
5) test_validators.py (30 tests unitarios)
6) CRITICA.md (análisis técnico de fortalezas/debilidades)
7) PROMPT_MEJORADO.md (este prompt con mejoras identificadas)
8) README.md (documentación completa)

RESTRICCIONES:
- Sin dependencias externas (excepto stdlib de Python + pycountry + re2)
- Compatible con Python 3.9+
- Performance: < 5ms p95 para validación simple
- Memoria: < 10MB para payloads de 1MB
- Thread-safe (puede usarse en async/concurrent)

CRITERIOS DE ÉXITO:
✅ 100% de fuzzing cases bloqueados correctamente
✅ 0 vulnerabilidades detectadas por OWASP ZAP
✅ Serialización idempotente (mismo input → mismo output JSON)
✅ Errores acumulados (1 request → todos los problemas)
✅ Documentación completa con ejemplos ejecutables
```

---

## 📈 **COMPARACIÓN: ANTES vs DESPUÉS**

| Aspecto | Implementación Actual | Propuesta Mejorada |
|---------|----------------------|-------------------|
| **Regex Safety** | ❌ Sin timeout | ✅ Timeout 500ms + re2 engine |
| **Payload Limit** | ❌ Sin límite | ✅ 1MB middleware |
| **HTML/SQL Escape** | ❌ Solo control chars | ✅ Full HTML + SQL escape |
| **Tags Whitelist** | ❌ Acepta cualquier string | ✅ Fuzzy matching con sugerencias |
| **Currency Support** | ❌ Solo 3 monedas | ✅ 170+ con pycountry |
| **Date Range** | ❌ Acepta 2999-12-31 | ✅ Rango 2000-ahora validado |
| **Unicode Normalization** | ❌ Sin normalizar | ✅ NFC normalizado |
| **Concurrent Testing** | ❌ Solo secuencial | ✅ 100 threads simultáneos |
| **Fuzzing Cases** | 10 casos básicos | 20 casos + property-based |
| **Performance** | No medido | < 5ms p95 con métricas |

---

## 💡 **CONCLUSIÓN**

**Implementación actual: 7.5/10**
- ✅ JSON Schema bien estructurado
- ✅ Serialización determinista
- ✅ Acumulación de errores
- ❌ Vulnerabilidades de seguridad (XSS, ReDoS)
- ❌ No escalable (solo 3 monedas)

**Con mejoras propuestas: 9.5/10**
- ✅ Seguro contra OWASP Top 10
- ✅ Escalable internacionalmente
- ✅ Performance garantizado
- ✅ Testing exhaustivo
- ⚠️ Complejidad aumentada (trade-off aceptable)
