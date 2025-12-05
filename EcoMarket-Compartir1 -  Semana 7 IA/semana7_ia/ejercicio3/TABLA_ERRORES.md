# Tabla de Errores de Validación

## 📋 Catálogo Completo de Errores

### 1. MISSING_REQUIRED - Campos Requeridos Faltantes

**Regla violada:** Campo obligatorio no proporcionado

**Ejemplo de entrada inválida:**
```json
{
  "price": 100,
  "currency": "MXN"
}
```
*Falta el campo `name` que es obligatorio*

**Respuesta HTTP:**
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
```

```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "msg": "Campos requeridos faltantes",
    "details": [
      {
        "field": "name",
        "issue": "Campo requerido no proporcionado"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-11-26T10:30:00.000Z",
    "requestId": "abc-123"
  }
}
```

---

### 2. INVALID_TYPE - Tipo de Dato Incorrecto

**Regla violada:** Se esperaba un tipo diferente

**Ejemplo de entrada inválida:**
```json
{
  "name": "Product",
  "price": "not-a-number",
  "currency": "USD"
}
```
*`price` debe ser number, no string*

**Respuesta HTTP:**
```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "msg": "Tipo de dato inválido",
    "details": [
      {
        "field": "price",
        "issue": "Se esperaba number, recibido string",
        "received": "not-a-number"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-11-26T10:30:00.000Z",
    "requestId": "def-456"
  }
}
```

---

### 3. OUT_OF_RANGE - Valor Fuera de Rango

**Regla violada:** `price >= 0`

**Ejemplo de entrada inválida:**
```json
{
  "name": "Product",
  "price": -10.50,
  "currency": "MXN"
}
```
*Precio negativo no permitido*

**Respuesta HTTP:**
```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "msg": "Violación de restricción",
    "details": [
      {
        "field": "price",
        "issue": "Debe ser >= 0",
        "received": -10.50
      }
    ]
  },
  "meta": {
    "timestamp": "2025-11-26T10:30:00.000Z",
    "requestId": "ghi-789"
  }
}
```

---

### 4. INVALID_LENGTH - Longitud Inválida

**Regla violada:** `name` debe tener entre 2 y 80 caracteres

**Ejemplo de entrada inválida:**
```json
{
  "name": "A",
  "price": 50,
  "currency": "EUR"
}
```
*Nombre demasiado corto (1 caracter < 2 mínimo)*

**Respuesta HTTP:**
```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "msg": "Longitud inválida",
    "details": [
      {
        "field": "name",
        "issue": "Mínimo 2 caracteres, recibido 1",
        "received": "A"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-11-26T10:30:00.000Z",
    "requestId": "jkl-012"
  }
}
```

---

### 5. INVALID_ENUM - Valor No Permitido

**Regla violada:** `currency` debe ser MXN, USD o EUR

**Ejemplo de entrada inválida:**
```json
{
  "name": "Product",
  "price": 100,
  "currency": "JPY"
}
```
*JPY no está en la lista de monedas soportadas*

**Respuesta HTTP:**
```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "msg": "Valor no permitido",
    "details": [
      {
        "field": "currency",
        "issue": "Debe ser uno de: MXN, USD, EUR",
        "received": "JPY"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-11-26T10:30:00.000Z",
    "requestId": "mno-345"
  }
}
```

---

### 6. ARRAY_TOO_LONG - Array Excede Máximo

**Regla violada:** `tags` máximo 10 elementos

**Ejemplo de entrada inválida:**
```json
{
  "name": "Product",
  "price": 100,
  "currency": "USD",
  "tags": ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11"]
}
```
*11 tags > límite de 10*

**Respuesta HTTP:**
```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "msg": "Array excede longitud máxima",
    "details": [
      {
        "field": "tags",
        "issue": "Máximo 10 elementos, recibido 11",
        "received": 11
      }
    ]
  },
  "meta": {
    "timestamp": "2025-11-26T10:30:00.000Z",
    "requestId": "pqr-678"
  }
}
```

---

### 7. DUPLICATE_VALUES - Elementos Duplicados

**Regla violada:** `tags` deben ser únicos

**Ejemplo de entrada inválida:**
```json
{
  "name": "Product",
  "price": 100,
  "currency": "MXN",
  "tags": ["electronics", "sale", "electronics"]
}
```
*"electronics" aparece dos veces*

**Respuesta HTTP:**
```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "msg": "Elementos duplicados no permitidos",
    "details": [
      {
        "field": "tags",
        "issue": "Todos los elementos deben ser únicos",
        "received": ["electronics", "sale", "electronics"]
      }
    ]
  },
  "meta": {
    "timestamp": "2025-11-26T10:30:00.000Z",
    "requestId": "stu-901"
  }
}
```

---

### 8. INVALID_FORMAT - Formato Inválido

**Regla violada:** Tags solo permiten `a-z0-9-`

**Ejemplo de entrada inválida:**
```json
{
  "name": "Product",
  "price": 100,
  "currency": "USD",
  "tags": ["Electronics", "SALE!", "new product"]
}
```
*Mayúsculas, signos de exclamación y espacios no permitidos*

**Respuesta HTTP:**
```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "msg": "Formato de tag inválido",
    "details": [
      {
        "field": "tags[0]",
        "issue": "Solo se permiten minúsculas y guiones (a-z0-9-)",
        "received": "Electronics"
      },
      {
        "field": "tags[1]",
        "issue": "Solo se permiten minúsculas y guiones (a-z0-9-)",
        "received": "SALE!"
      },
      {
        "field": "tags[2]",
        "issue": "Solo se permiten minúsculas y guiones (a-z0-9-)",
        "received": "new product"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-11-26T10:30:00.000Z",
    "requestId": "vwx-234"
  }
}
```

---

### 9. INVALID_DATE_FORMAT - Fecha No ISO-8601

**Regla violada:** `createdAt` debe ser ISO-8601 UTC

**Ejemplo de entrada inválida:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Product",
  "price": 100,
  "currency": "USD",
  "createdAt": "2025-11-26 10:30:00"
}
```
*Falta "T" entre fecha y hora, y falta "Z" al final*

**Respuesta HTTP:**
```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "msg": "Formato de fecha inválido",
    "details": [
      {
        "field": "createdAt",
        "issue": "Debe estar en formato ISO-8601: YYYY-MM-DDTHH:mm:ss.sssZ",
        "received": "2025-11-26 10:30:00"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-11-26T10:30:00.000Z",
    "requestId": "yz1-567"
  }
}
```

---

### 10. ADDITIONAL_PROPERTIES - Propiedades No Permitidas

**Regla violada:** `additionalProperties: false` en schema

**Ejemplo de entrada inválida:**
```json
{
  "name": "Product",
  "price": 100,
  "currency": "USD",
  "extraField": "not-allowed",
  "anotherExtra": 123
}
```
*Campos no definidos en el schema*

**Respuesta HTTP:**
```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "msg": "Propiedades adicionales no permitidas",
    "details": [
      {
        "field": "extraField",
        "issue": "Propiedad no definida en el schema"
      },
      {
        "field": "anotherExtra",
        "issue": "Propiedad no definida en el schema"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-11-26T10:30:00.000Z",
    "requestId": "234-890"
  }
}
```

---

## 📊 Tabla Resumen

| # | Código Error | Regla Violada | Campo Común | HTTP |
|---|--------------|---------------|-------------|------|
| 1 | VALIDATION_ERROR | Campo requerido faltante | `name`, `price`, `currency` | 400 |
| 2 | VALIDATION_ERROR | Tipo incorrecto | `price` (string en vez de number) | 400 |
| 3 | VALIDATION_ERROR | Valor < 0 | `price` | 400 |
| 4 | VALIDATION_ERROR | Longitud < 2 o > 80 | `name` | 400 |
| 5 | VALIDATION_ERROR | Moneda no soportada | `currency` (no MXN/USD/EUR) | 400 |
| 6 | VALIDATION_ERROR | Array > 10 elementos | `tags` | 400 |
| 7 | VALIDATION_ERROR | Elementos duplicados | `tags` | 400 |
| 8 | VALIDATION_ERROR | Patrón inválido | `tags` (mayúsculas, espacios) | 400 |
| 9 | VALIDATION_ERROR | Formato de fecha | `createdAt` (no ISO-8601) | 400 |
| 10 | VALIDATION_ERROR | Campos extra | Cualquier campo no definido | 400 |

---

## 🎯 Matriz de Validación Completa

| Campo | Requerido | Tipo | Restricciones | Errores Posibles |
|-------|-----------|------|---------------|------------------|
| `id` | ✅ (en respuesta) | string (UUID) | UUID v4 válido | INVALID_FORMAT |
| `name` | ✅ | string | 2-80 chars, alfanumérico + puntuación | MISSING_REQUIRED, INVALID_LENGTH, INVALID_FORMAT |
| `price` | ✅ | number | >= 0, <= 999999999.99, 2 decimales | MISSING_REQUIRED, INVALID_TYPE, OUT_OF_RANGE |
| `currency` | ✅ | string | MXN \| USD \| EUR | MISSING_REQUIRED, INVALID_ENUM |
| `tags` | ❌ | array[string] | 0-10 items, únicos, a-z0-9- | ARRAY_TOO_LONG, DUPLICATE_VALUES, INVALID_FORMAT |
| `createdAt` | ✅ (en respuesta) | string | ISO-8601 UTC | INVALID_DATE_FORMAT |

---

## 🔍 Ejemplos de Curl para Testing

### ✅ Caso Exitoso
```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15 Pro",
    "price": 999.00,
    "currency": "USD",
    "tags": ["electronics", "smartphones", "apple"]
  }'
```

### ❌ Error: Precio Negativo
```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product",
    "price": -10.50,
    "currency": "MXN"
  }'
```

### ❌ Error: Tags Duplicados
```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product",
    "price": 100,
    "currency": "USD",
    "tags": ["electronics", "sale", "electronics"]
  }'
```

### ❌ Error: Moneda Inválida
```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product",
    "price": 100,
    "currency": "JPY"
  }'
```

---

## 🧪 Estrategias de Testing

### 1. **Boundary Testing**
- Probar límites exactos (name = 2 chars, name = 80 chars)
- Probar justo fuera de límites (name = 1 char, name = 81 chars)

### 2. **Type Coercion**
- Enviar "100" (string) cuando se espera 100 (number)
- Enviar true/false en campos string
- Enviar null en campos requeridos

### 3. **Edge Cases**
- Strings vacíos (`""`)
- Arrays vacíos (`[]`)
- Valores muy grandes (price = 999999999999)
- Unicode especial (`"Producto 日本"`)

### 4. **Combinaciones Múltiples**
- Múltiples errores simultáneos (price negativo + currency inválida + name corto)
- Verificar que `details` contiene todos los errores

---

## 💡 Notas de Implementación

### Orden de Validación Recomendado:
1. **Verificar campos requeridos** → devolver todos los faltantes juntos
2. **Verificar tipos** → antes de validar restricciones
3. **Validar restricciones** → rangos, longitudes, formatos
4. **Acumular errores** → devolver todos los problemas en una sola respuesta

### Serialización Determinista:
```python
# Orden fijo de propiedades
PROPERTY_ORDER = ["id", "name", "price", "currency", "tags", "createdAt"]

def serialize(product):
    return {key: product[key] for key in PROPERTY_ORDER if key in product and product[key] is not None}
```

### Sanitización:
- **name**: Eliminar espacios múltiples, trim, eliminar control chars
- **tags**: Convertir a lowercase, trim
- **currency**: Convertir a uppercase
- **price**: Redondear a 2 decimales

---

**Autor:** Ejercicio 3 - Semana 7 IA  
**Última actualización:** 26 Nov 2025
