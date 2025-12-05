# Scripts de Testing Manual - Ejercicio 4

Colección de comandos curl para probar la API manualmente.

---

## 🚀 PREREQUISITO

API debe estar corriendo:
```bash
uvicorn api_complete:app --reload --port 8000
```

---

## 1. HEALTH CHECK

```bash
curl http://localhost:8000/
```

**Respuesta esperada:**
```json
{
  "data": {
    "status": "healthy",
    "version": "1.0.0"
  },
  "error": null
}
```

---

## 2. CICLO CRUD COMPLETO

### 2.1 CREATE - Crear Producto

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

**Guardar el `id` de la respuesta para los siguientes pasos.**

---

### 2.2 READ - Obtener Producto

```bash
# Reemplazar {PRODUCT_ID} con el ID del paso anterior
curl http://localhost:8000/api/v1/products/{PRODUCT_ID}
```

**Ejemplo:**
```bash
curl http://localhost:8000/api/v1/products/550e8400-e29b-41d4-a716-446655440000
```

---

### 2.3 LIST - Listar Todos

```bash
curl http://localhost:8000/api/v1/products
```

**Con paginación:**
```bash
curl "http://localhost:8000/api/v1/products?skip=0&limit=10"
```

---

### 2.4 UPDATE - Actualizar Producto

```bash
# Sin control de versión (always succeeds)
curl -X PUT http://localhost:8000/api/v1/products/{PRODUCT_ID} \
  -H "Content-Type: application/json" \
  -d '{
    "price": 899.00
  }'
```

**Con control de versión (optimistic locking):**
```bash
# VERSION debe ser la version actual del producto
curl -X PUT http://localhost:8000/api/v1/products/{PRODUCT_ID} \
  -H "Content-Type: application/json" \
  -H 'If-Match: "1"' \
  -d '{
    "price": 899.00
  }'
```

---

### 2.5 DELETE - Eliminar Producto

```bash
curl -X DELETE http://localhost:8000/api/v1/products/{PRODUCT_ID}
```

**Respuesta esperada:** 204 No Content (sin body)

---

## 3. TESTS DE VALIDACIÓN

### 3.1 ❌ Campos Requeridos Faltantes

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product"
  }'
```

**Respuesta esperada:** 422 Unprocessable Entity

---

### 3.2 ❌ Precio Negativo

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product",
    "price": -10.50,
    "currency": "USD"
  }'
```

**Respuesta esperada:** 422

---

### 3.3 ❌ Moneda Inválida

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product",
    "price": 100,
    "currency": "JPY"
  }'
```

**Respuesta esperada:** 422

---

### 3.4 ❌ Tags Duplicados

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

**Respuesta esperada:** 400 Bad Request

---

### 3.5 ❌ UUID Inválido

```bash
curl http://localhost:8000/api/v1/products/not-a-uuid
```

**Respuesta esperada:** 400 Bad Request
```json
{
  "error": {
    "code": "INVALID_UUID",
    "msg": "UUID inválido: not-a-uuid"
  }
}
```

---

### 3.6 ❌ Producto No Existe

```bash
curl http://localhost:8000/api/v1/products/00000000-0000-0000-0000-000000000000
```

**Respuesta esperada:** 404 Not Found
```json
{
  "error": {
    "code": "NOT_FOUND",
    "msg": "Producto 00000000-0000-0000-0000-000000000000 no encontrado"
  }
}
```

---

## 4. TESTS DE CONCURRENCIA

### 4.1 Optimistic Locking - Conflicto de Versión

**Paso 1:** Crear producto
```bash
PRODUCT_ID=$(curl -s -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 100, "currency": "USD"}' \
  | jq -r '.data.id')

echo "Product ID: $PRODUCT_ID"
```

**Paso 2:** Usuario 1 actualiza (version 1 → 2)
```bash
curl -X PUT http://localhost:8000/api/v1/products/$PRODUCT_ID \
  -H "Content-Type: application/json" \
  -H 'If-Match: "1"' \
  -d '{"price": 90}'
```

**Paso 3:** Usuario 2 intenta actualizar con version vieja (DEBE FALLAR)
```bash
curl -X PUT http://localhost:8000/api/v1/products/$PRODUCT_ID \
  -H "Content-Type: application/json" \
  -H 'If-Match: "1"' \
  -d '{"price": 80}'
```

**Respuesta esperada:** 409 Conflict
```json
{
  "error": {
    "code": "CONFLICT",
    "msg": "Conflicto de versión. Esperado: 1, actual: 2",
    "currentVersion": 2
  }
}
```

---

### 4.2 Creación Concurrente (Bash Loop)

```bash
# Crear 10 productos simultáneamente
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/v1/products \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"Product $i\", \"price\": $((100 + i)), \"currency\": \"USD\"}" &
done
wait

# Listar para verificar
curl http://localhost:8000/api/v1/products | jq '.data.total'
```

**Resultado esperado:** `total: 10`

---

## 5. TESTS DE PAGINACIÓN

### 5.1 Crear Datos de Prueba

```bash
# Crear 5 productos
for i in {1..5}; do
  curl -s -X POST http://localhost:8000/api/v1/products \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"Product $i\", \"price\": $((100 + i)), \"currency\": \"USD\"}" > /dev/null
done
```

### 5.2 Página 1 (primeros 2)

```bash
curl "http://localhost:8000/api/v1/products?skip=0&limit=2" | jq '.data.items | length'
```

**Resultado esperado:** `2`

### 5.3 Página 2 (siguientes 2)

```bash
curl "http://localhost:8000/api/v1/products?skip=2&limit=2" | jq '.data.items | length'
```

**Resultado esperado:** `2`

### 5.4 ❌ Paginación Inválida

```bash
# skip negativo
curl "http://localhost:8000/api/v1/products?skip=-1"

# limit > 100
curl "http://localhost:8000/api/v1/products?limit=101"
```

**Respuesta esperada:** 400 Bad Request

---

## 6. EDGE CASES

### 6.1 Precio Exactamente 0

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Free Product",
    "price": 0,
    "currency": "USD"
  }'
```

**Respuesta esperada:** 201 Created ✅

---

### 6.2 Nombre de 2 Caracteres (Mínimo)

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AB",
    "price": 10,
    "currency": "USD"
  }'
```

**Respuesta esperada:** 201 Created ✅

---

### 6.3 Nombre de 80 Caracteres (Máximo)

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"$(printf 'A%.0s' {1..80})\",
    \"price\": 10,
    \"currency\": \"USD\"
  }"
```

**Respuesta esperada:** 201 Created ✅

---

### 6.4 10 Tags (Máximo)

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product",
    "price": 100,
    "currency": "USD",
    "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10"]
  }'
```

**Respuesta esperada:** 201 Created ✅

---

### 6.5 Currency en Minúsculas (Normalización)

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product",
    "price": 100,
    "currency": "usd"
  }'
```

**Respuesta esperada:** 201 Created, `currency: "USD"` (normalizado)

---

## 7. UTILS PARA TESTING

### 7.1 Limpiar Base de Datos

```bash
curl -X POST http://localhost:8000/api/v1/_test/clear
```

---

### 7.2 Ver Estadísticas

```bash
curl http://localhost:8000/api/v1/_test/stats
```

**Respuesta:**
```json
{
  "data": {
    "productCount": 5,
    "lockCount": 5
  }
}
```

---

### 7.3 Crear Múltiples Productos (Helper)

```bash
#!/bin/bash
# create_products.sh

BASE_URL="http://localhost:8000/api/v1"

products=(
  '{"name": "Laptop ThinkPad", "price": 1299.99, "currency": "USD", "tags": ["electronics", "computers"]}'
  '{"name": "Mouse Logitech", "price": 79.99, "currency": "USD", "tags": ["electronics", "accessories"]}'
  '{"name": "Teclado Mecánico", "price": 149.50, "currency": "MXN", "tags": ["electronics"]}'
)

for product in "${products[@]}"; do
  echo "Creating: $product"
  curl -s -X POST "$BASE_URL/products" \
    -H "Content-Type: application/json" \
    -d "$product" | jq '.data.id'
done
```

**Uso:**
```bash
chmod +x create_products.sh
./create_products.sh
```

---

### 7.4 Eliminar Todos los Productos (Helper)

```bash
#!/bin/bash
# delete_all_products.sh

BASE_URL="http://localhost:8000/api/v1"

# Obtener todos los IDs
IDS=$(curl -s "$BASE_URL/products?limit=100" | jq -r '.data.items[].id')

# Eliminar cada uno
for id in $IDS; do
  echo "Deleting: $id"
  curl -s -X DELETE "$BASE_URL/products/$id"
done

echo "All products deleted"
```

**Uso:**
```bash
chmod +x delete_all_products.sh
./delete_all_products.sh
```

---

### 7.5 Medir Latencia (Benchmark)

```bash
#!/bin/bash
# benchmark.sh

BASE_URL="http://localhost:8000/api/v1"
ITERATIONS=100

echo "Benchmarking CREATE..."
for i in $(seq 1 $ITERATIONS); do
  curl -s -w "%{time_total}\n" -o /dev/null \
    -X POST "$BASE_URL/products" \
    -H "Content-Type: application/json" \
    -d '{"name": "Test", "price": 100, "currency": "USD"}'
done | awk '{ sum += $1; n++ } END { print "Average: " sum/n*1000 "ms" }'
```

**Uso:**
```bash
chmod +x benchmark.sh
./benchmark.sh
```

---

## 8. POWERSHELL EQUIVALENTES

### 8.1 CREATE (PowerShell)

```powershell
$body = @{
    name = "iPhone 15 Pro"
    price = 999.00
    currency = "USD"
    tags = @("electronics", "smartphones", "apple")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

---

### 8.2 READ (PowerShell)

```powershell
$productId = "550e8400-e29b-41d4-a716-446655440000"
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products/$productId" `
    -Method Get
```

---

### 8.3 LIST (PowerShell)

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products" `
    -Method Get
```

---

### 8.4 UPDATE (PowerShell)

```powershell
$productId = "550e8400-e29b-41d4-a716-446655440000"
$body = @{ price = 899.00 } | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products/$productId" `
    -Method Put `
    -ContentType "application/json" `
    -Body $body
```

---

### 8.5 DELETE (PowerShell)

```powershell
$productId = "550e8400-e29b-41d4-a716-446655440000"
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products/$productId" `
    -Method Delete
```

---

### 8.6 Crear 10 Productos Concurrentemente (PowerShell)

```powershell
$jobs = 1..10 | ForEach-Object {
    Start-Job -ScriptBlock {
        param($i)
        $body = @{
            name = "Product $i"
            price = 100 + $i
            currency = "USD"
        } | ConvertTo-Json
        
        Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products" `
            -Method Post `
            -ContentType "application/json" `
            -Body $body
    } -ArgumentList $_
}

$jobs | Wait-Job | Receive-Job
```

---

## 📊 VALIDAR RESULTADOS CON JQ

### Extraer Solo IDs

```bash
curl -s http://localhost:8000/api/v1/products | jq -r '.data.items[].id'
```

### Contar Productos

```bash
curl -s http://localhost:8000/api/v1/products | jq '.data.total'
```

### Filtrar por Precio > 500

```bash
curl -s http://localhost:8000/api/v1/products | \
  jq '.data.items[] | select(.price > 500) | {name, price}'
```

### Ver Solo Nombres y Precios

```bash
curl -s http://localhost:8000/api/v1/products | \
  jq '.data.items[] | "\(.name): $\(.price) \(.currency)"'
```

---

**Autor:** Ejercicio 4 - Semana 7 IA  
**Fecha:** 26 Nov 2025
