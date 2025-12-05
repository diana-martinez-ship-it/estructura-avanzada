"""
Casos de borde y pruebas - Ejercicio 1
Pruebas de validación, errores y edge cases
"""
import pytest
from fastapi.testclient import TestClient
from api import app
from uuid import uuid4

client = TestClient(app)


# ============== CASOS EXITOSOS ==============

def test_create_product_success():
    """✅ Crear producto válido"""
    response = client.post("/api/v1/products", json={
        "name": "Laptop Ecológica",
        "price": 899.99,
        "currency": "MXN",
        "tags": ["tecnología", "sostenible"]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["error"] is None
    assert data["data"]["name"] == "Laptop Ecológica"
    assert data["data"]["price"] == 899.99
    assert "id" in data["data"]


def test_list_products_empty():
    """✅ Listar productos sin datos"""
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert data["error"] is None
    assert isinstance(data["data"], list)
    assert "total" in data["meta"]


def test_full_crud_cycle():
    """✅ Ciclo completo: crear → leer → actualizar → eliminar"""
    # Crear
    create_response = client.post("/api/v1/products", json={
        "name": "Producto Temporal",
        "price": 50.0,
        "currency": "USD"
    })
    assert create_response.status_code == 201
    product_id = create_response.json()["data"]["id"]
    
    # Leer
    get_response = client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == 200
    assert get_response.json()["data"]["name"] == "Producto Temporal"
    
    # Actualizar
    update_response = client.put(f"/api/v1/products/{product_id}", json={
        "name": "Producto Actualizado"
    })
    assert update_response.status_code == 200
    assert update_response.json()["data"]["name"] == "Producto Actualizado"
    
    # Eliminar
    delete_response = client.delete(f"/api/v1/products/{product_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["data"]["deleted"] is True


# ============== CASOS DE BORDE ==============

def test_get_nonexistent_product():
    """❌ CASO BORDE: ID inexistente"""
    fake_id = str(uuid4())
    response = client.get(f"/api/v1/products/{fake_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["data"] is None
    assert data["error"]["code"] == "NOT_FOUND"
    assert "no encontrado" in data["error"]["msg"].lower()


def test_create_product_empty_body():
    """❌ CASO BORDE: Body vacío"""
    response = client.post("/api/v1/products", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert len(data["error"]["details"]) > 0


def test_create_product_missing_required_fields():
    """❌ CASO BORDE: Campos requeridos faltantes"""
    response = client.post("/api/v1/products", json={
        "currency": "MXN"  # Falta name y price
    })
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    # Debe haber errores para 'name' y 'price'
    fields_with_errors = [d["field"] for d in data["error"]["details"]]
    assert "name" in fields_with_errors
    assert "price" in fields_with_errors


def test_create_product_invalid_types():
    """❌ CASO BORDE: Tipos de datos erróneos"""
    response = client.post("/api/v1/products", json={
        "name": "Producto",
        "price": "INVALID",  # String en lugar de número
        "currency": "MXN"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_product_negative_price():
    """❌ VALIDACIÓN: Precio negativo"""
    response = client.post("/api/v1/products", json={
        "name": "Producto Gratis",
        "price": -10.0,
        "currency": "MXN"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert any("price" in d.get("field", "") for d in data["error"]["details"])


def test_create_product_name_too_short():
    """❌ VALIDACIÓN: Nombre muy corto (< 2 caracteres)"""
    response = client.post("/api/v1/products", json={
        "name": "A",
        "price": 100.0,
        "currency": "USD"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_product_name_too_long():
    """❌ VALIDACIÓN: Nombre muy largo (> 80 caracteres)"""
    response = client.post("/api/v1/products", json={
        "name": "A" * 100,
        "price": 100.0,
        "currency": "EUR"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_product_too_many_tags():
    """❌ VALIDACIÓN: Más de 10 tags"""
    response = client.post("/api/v1/products", json={
        "name": "Producto con muchos tags",
        "price": 50.0,
        "currency": "MXN",
        "tags": [f"tag{i}" for i in range(15)]
    })
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_product_invalid_currency():
    """❌ VALIDACIÓN: Moneda no soportada"""
    response = client.post("/api/v1/products", json={
        "name": "Producto",
        "price": 100.0,
        "currency": "GBP"  # No está en el enum
    })
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_product_xss_attempt():
    """❌ SEGURIDAD: Intento de XSS en nombre"""
    response = client.post("/api/v1/products", json={
        "name": "Producto <script>alert('xss')</script>",
        "price": 100.0,
        "currency": "MXN"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    # El validador debe detectar el patrón peligroso
    assert any("sospechoso" in d.get("message", "").lower() 
               for d in data["error"]["details"])


def test_update_nonexistent_product():
    """❌ CASO BORDE: Actualizar producto inexistente"""
    fake_id = str(uuid4())
    response = client.put(f"/api/v1/products/{fake_id}", json={
        "name": "Nuevo nombre"
    })
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "NOT_FOUND"


def test_delete_nonexistent_product():
    """❌ CASO BORDE: Eliminar producto inexistente"""
    fake_id = str(uuid4())
    response = client.delete(f"/api/v1/products/{fake_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "NOT_FOUND"


def test_list_products_with_filters():
    """✅ Listar con filtros válidos"""
    # Primero crear algunos productos
    client.post("/api/v1/products", json={
        "name": "Producto Caro",
        "price": 1000.0,
        "currency": "USD"
    })
    client.post("/api/v1/products", json={
        "name": "Producto Barato",
        "price": 10.0,
        "currency": "MXN"
    })
    
    # Filtrar por precio mínimo
    response = client.get("/api/v1/products?min_price=500")
    assert response.status_code == 200
    data = response.json()
    assert all(p["price"] >= 500 for p in data["data"])


def test_list_products_invalid_page():
    """❌ CASO BORDE: Página inválida (< 1)"""
    response = client.get("/api/v1/products?page=0")
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_list_products_invalid_limit():
    """❌ CASO BORDE: Límite fuera de rango"""
    response = client.get("/api/v1/products?limit=200")  # Máximo es 100
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_invalid_uuid_format():
    """❌ CASO BORDE: UUID con formato inválido"""
    response = client.get("/api/v1/products/not-a-uuid")
    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


# ============== TABLA DE RESUMEN ==============

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  RESUMEN DE CASOS DE BORDE - Ejercicio 1")
    print("="*70 + "\n")
    
    casos = [
        ("✅ Crear producto válido", "201", "Producto creado exitosamente"),
        ("✅ Listar productos vacío", "200", "Lista vacía con meta correcta"),
        ("✅ CRUD completo", "201→200→200→200", "Ciclo completo funcional"),
        ("❌ ID inexistente (GET)", "404", "NOT_FOUND con mensaje"),
        ("❌ Body vacío (POST)", "400", "VALIDATION_ERROR"),
        ("❌ Campos faltantes", "400", "VALIDATION_ERROR con detalles"),
        ("❌ Tipos erróneos", "400", "VALIDATION_ERROR"),
        ("❌ Precio negativo", "400", "VALIDATION_ERROR en field:price"),
        ("❌ Nombre < 2 chars", "400", "VALIDATION_ERROR en minLength"),
        ("❌ Nombre > 80 chars", "400", "VALIDATION_ERROR en maxLength"),
        ("❌ Más de 10 tags", "400", "VALIDATION_ERROR en maxItems"),
        ("❌ Moneda inválida", "400", "VALIDATION_ERROR en enum"),
        ("❌ XSS attempt", "400", "Sanitización detecta patrón"),
        ("❌ Actualizar inexistente", "404", "NOT_FOUND"),
        ("❌ Eliminar inexistente", "404", "NOT_FOUND"),
        ("❌ Página < 1", "400", "VALIDATION_ERROR en página"),
        ("❌ Límite > 100", "400", "VALIDATION_ERROR en límite"),
        ("❌ UUID inválido", "422", "VALIDATION_ERROR en formato"),
    ]
    
    for caso, status, resultado in casos:
        print(f"{caso:40s} | Status: {status:15s} | {resultado}")
    
    print("\n" + "="*70)
    print(f"  TOTAL: {len(casos)} casos de borde documentados")
    print("="*70 + "\n")
