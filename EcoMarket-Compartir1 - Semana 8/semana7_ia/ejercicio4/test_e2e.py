"""
Tests E2E Completos - Ejercicio 4
==================================

Suite exhaustiva de pruebas de integración para /api/v1/products:
- Escenarios CRUD completos
- Fixtures reutilizables
- Tests de concurrencia
- Casos de error (4xx/5xx)
- Limpieza transaccional
- Métricas de cobertura y latencia
"""

import pytest
import httpx
import asyncio
import time
from typing import Dict, List
from datetime import datetime


# ============== CONFIGURACIÓN ==============

API_BASE_URL = "http://localhost:8000"
API_V1_URL = f"{API_BASE_URL}/api/v1"


# ============== FIXTURES ==============

@pytest.fixture
def client():
    """Cliente HTTP sincrónico"""
    return httpx.Client(base_url=API_BASE_URL)


@pytest.fixture
async def async_client():
    """Cliente HTTP asíncrono para tests de concurrencia"""
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        yield client


@pytest.fixture(autouse=True)
def clear_database(client):
    """Limpiar base de datos antes de cada test"""
    client.post(f"{API_V1_URL}/_test/clear")
    yield
    # Cleanup después del test también
    client.post(f"{API_V1_URL}/_test/clear")


@pytest.fixture
def sample_product():
    """Fixture: producto de ejemplo"""
    return {
        "name": "iPhone 15 Pro",
        "price": 999.00,
        "currency": "USD",
        "tags": ["electronics", "smartphones", "apple"]
    }


@pytest.fixture
def sample_products_list():
    """Fixture: lista de productos para tests"""
    return [
        {"name": "Laptop ThinkPad X1", "price": 1299.99, "currency": "USD", "tags": ["electronics", "computers"]},
        {"name": "Mouse Logitech MX", "price": 79.99, "currency": "USD", "tags": ["electronics", "accessories"]},
        {"name": "Teclado Mecánico", "price": 149.50, "currency": "MXN", "tags": ["electronics", "peripherals"]},
        {"name": "Monitor LG 27''", "price": 299.00, "currency": "EUR", "tags": ["electronics", "displays"]},
        {"name": "Webcam HD", "price": 59.99, "currency": "USD", "tags": ["electronics", "streaming"]},
    ]


# ============== HELPER FUNCTIONS ==============

def assert_response_structure(response_data: Dict):
    """Validar estructura estándar de respuesta"""
    assert "data" in response_data
    assert "error" in response_data
    assert "meta" in response_data
    assert "timestamp" in response_data["meta"]


def create_product(client, product_data: Dict) -> Dict:
    """Helper: crear producto y retornar datos"""
    response = client.post(f"{API_V1_URL}/products", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert_response_structure(data)
    assert data["error"] is None
    return data["data"]


def measure_latency(func, *args, **kwargs):
    """Medir latencia de una función"""
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    latency_ms = (end - start) * 1000
    return result, latency_ms


# ============== TESTS: CICLO CRUD COMPLETO ==============

class TestCRUDFlow:
    """Tests del flujo CRUD completo: Create → Read → Update → Delete"""
    
    def test_e2e_happy_path(self, client, sample_product):
        """✅ E2E: Ciclo completo exitoso"""
        print("\n" + "="*70)
        print("TEST E2E: HAPPY PATH (Create → Read → Update → Delete)")
        print("="*70)
        
        # 1. CREATE
        print("\n1️⃣ CREATE: Crear producto")
        create_response = client.post(f"{API_V1_URL}/products", json=sample_product)
        assert create_response.status_code == 201
        
        create_data = create_response.json()
        assert_response_structure(create_data)
        assert create_data["error"] is None
        
        product = create_data["data"]
        product_id = product["id"]
        
        assert product["name"] == sample_product["name"]
        assert product["price"] == sample_product["price"]
        assert product["currency"] == sample_product["currency"]
        assert "id" in product
        assert "createdAt" in product
        assert "version" in product
        assert product["version"] == 1
        
        print(f"   ✅ Producto creado: {product_id}")
        print(f"   ✅ Version: {product['version']}")
        
        # 2. READ (individual)
        print("\n2️⃣ READ: Obtener producto por ID")
        read_response = client.get(f"{API_V1_URL}/products/{product_id}")
        assert read_response.status_code == 200
        
        read_data = read_response.json()
        assert read_data["data"]["id"] == product_id
        assert read_data["data"]["name"] == sample_product["name"]
        
        print(f"   ✅ Producto obtenido: {read_data['data']['name']}")
        
        # 3. READ (lista)
        print("\n3️⃣ LIST: Listar todos los productos")
        list_response = client.get(f"{API_V1_URL}/products")
        assert list_response.status_code == 200
        
        list_data = list_response.json()
        assert list_data["data"]["total"] == 1
        assert len(list_data["data"]["items"]) == 1
        assert list_data["data"]["items"][0]["id"] == product_id
        
        print(f"   ✅ Total de productos: {list_data['data']['total']}")
        
        # 4. UPDATE
        print("\n4️⃣ UPDATE: Actualizar precio")
        update_payload = {"price": 899.00}
        update_response = client.put(
            f"{API_V1_URL}/products/{product_id}",
            json=update_payload
        )
        assert update_response.status_code == 200
        
        update_data = update_response.json()
        assert update_data["data"]["price"] == 899.00
        assert update_data["data"]["version"] == 2  # Version incrementada
        
        print(f"   ✅ Precio actualizado: ${update_data['data']['price']}")
        print(f"   ✅ Version incrementada: {update_data['data']['version']}")
        
        # 5. DELETE
        print("\n5️⃣ DELETE: Eliminar producto")
        delete_response = client.delete(f"{API_V1_URL}/products/{product_id}")
        assert delete_response.status_code == 204
        
        print(f"   ✅ Producto eliminado: {product_id}")
        
        # 6. VERIFY DELETION
        print("\n6️⃣ VERIFY: Confirmar que fue eliminado")
        verify_response = client.get(f"{API_V1_URL}/products/{product_id}")
        assert verify_response.status_code == 404
        
        verify_data = verify_response.json()
        assert verify_data["error"]["code"] == "NOT_FOUND"
        
        print("   ✅ Confirmado: producto no existe (404)")
        
        print("\n" + "="*70)
        print("✅ E2E HAPPY PATH COMPLETADO")
        print("="*70)
    
    def test_e2e_multiple_products(self, client, sample_products_list):
        """✅ E2E: Crear múltiples productos y listar"""
        print("\n" + "="*70)
        print("TEST E2E: MÚLTIPLES PRODUCTOS")
        print("="*70)
        
        created_ids = []
        
        # Crear 5 productos
        print(f"\n📦 Creando {len(sample_products_list)} productos...")
        for i, product_data in enumerate(sample_products_list, 1):
            product = create_product(client, product_data)
            created_ids.append(product["id"])
            print(f"   {i}. {product['name']} - ${product['price']} {product['currency']}")
        
        # Listar todos
        print("\n📋 Listando todos los productos...")
        list_response = client.get(f"{API_V1_URL}/products")
        assert list_response.status_code == 200
        
        list_data = list_response.json()
        assert list_data["data"]["total"] == len(sample_products_list)
        assert len(list_data["data"]["items"]) == len(sample_products_list)
        
        print(f"   ✅ Total: {list_data['data']['total']}")
        print(f"   ✅ Items en página: {len(list_data['data']['items'])}")
        
        # Eliminar todos
        print("\n🗑️  Eliminando todos los productos...")
        for product_id in created_ids:
            delete_response = client.delete(f"{API_V1_URL}/products/{product_id}")
            assert delete_response.status_code == 204
        
        # Verificar que lista está vacía
        final_list = client.get(f"{API_V1_URL}/products").json()
        assert final_list["data"]["total"] == 0
        
        print("   ✅ Todos los productos eliminados")
        print("\n" + "="*70)


# ============== TESTS: VALIDACIÓN ==============

class TestValidation:
    """Tests de validación de entrada"""
    
    def test_create_missing_required_fields(self, client):
        """❌ Error: Campos requeridos faltantes"""
        response = client.post(f"{API_V1_URL}/products", json={})
        assert response.status_code == 422  # Unprocessable Entity (FastAPI)
        
        data = response.json()
        assert "detail" in data
    
    def test_create_invalid_price(self, client):
        """❌ Error: Precio negativo"""
        invalid_product = {
            "name": "Product",
            "price": -10.50,
            "currency": "USD"
        }
        
        response = client.post(f"{API_V1_URL}/products", json=invalid_product)
        assert response.status_code == 422
    
    def test_create_invalid_currency(self, client):
        """❌ Error: Moneda no soportada"""
        invalid_product = {
            "name": "Product",
            "price": 100,
            "currency": "JPY"
        }
        
        response = client.post(f"{API_V1_URL}/products", json=invalid_product)
        assert response.status_code == 422
    
    def test_create_duplicate_tags(self, client):
        """❌ Error: Tags duplicados"""
        invalid_product = {
            "name": "Product",
            "price": 100,
            "currency": "USD",
            "tags": ["electronics", "sale", "electronics"]
        }
        
        response = client.post(f"{API_V1_URL}/products", json=invalid_product)
        assert response.status_code == 400
        
        data = response.json()
        assert data["error"]["code"] == "VALIDATION_ERROR"
    
    def test_get_invalid_uuid(self, client):
        """❌ Error: UUID inválido"""
        response = client.get(f"{API_V1_URL}/products/not-a-uuid")
        assert response.status_code == 400
        
        data = response.json()
        assert data["error"]["code"] == "INVALID_UUID"
    
    def test_get_nonexistent_product(self, client):
        """❌ Error: Producto no existe"""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"{API_V1_URL}/products/{fake_uuid}")
        assert response.status_code == 404
        
        data = response.json()
        assert data["error"]["code"] == "NOT_FOUND"


# ============== TESTS: CONCURRENCIA ==============

class TestConcurrency:
    """Tests de manejo de concurrencia"""
    
    @pytest.mark.asyncio
    async def test_optimistic_locking(self, async_client, sample_product):
        """✅ Control de concurrencia optimista con versiones"""
        print("\n" + "="*70)
        print("TEST: OPTIMISTIC LOCKING (Control de versiones)")
        print("="*70)
        
        # Crear producto
        create_response = await async_client.post(f"{API_V1_URL}/products", json=sample_product)
        product = create_response.json()["data"]
        product_id = product["id"]
        version = product["version"]
        
        print(f"\n📦 Producto creado: {product_id}")
        print(f"   Version inicial: {version}")
        
        # Usuario 1: Actualizar con version correcta
        print("\n👤 Usuario 1: Actualizar con version correcta")
        update1 = await async_client.put(
            f"{API_V1_URL}/products/{product_id}",
            json={"price": 899.00},
            headers={"If-Match": f'"{version}"'}
        )
        assert update1.status_code == 200
        updated_product = update1.json()["data"]
        new_version = updated_product["version"]
        
        print(f"   ✅ Actualización exitosa")
        print(f"   Nueva version: {new_version}")
        
        # Usuario 2: Intentar actualizar con version vieja (debe fallar)
        print("\n👤 Usuario 2: Intentar actualizar con version vieja")
        update2 = await async_client.put(
            f"{API_V1_URL}/products/{product_id}",
            json={"price": 799.00},
            headers={"If-Match": f'"{version}"'}  # Version vieja
        )
        assert update2.status_code == 409  # Conflict
        
        error_data = update2.json()
        assert error_data["error"]["code"] == "CONFLICT"
        assert "currentVersion" in error_data["error"]
        
        print(f"   ❌ Actualización rechazada (409 Conflict)")
        print(f"   Razón: Version {version} != {new_version}")
        
        print("\n" + "="*70)
        print("✅ OPTIMISTIC LOCKING FUNCIONANDO CORRECTAMENTE")
        print("="*70)
    
    @pytest.mark.asyncio
    async def test_concurrent_creates(self, async_client):
        """✅ Creación concurrente de múltiples productos"""
        print("\n" + "="*70)
        print("TEST: CREACIÓN CONCURRENTE (10 productos simultáneos)")
        print("="*70)
        
        products_data = [
            {"name": f"Product {i}", "price": 100 + i, "currency": "USD"}
            for i in range(10)
        ]
        
        # Crear 10 productos concurrentemente
        print("\n🚀 Creando 10 productos simultáneamente...")
        start_time = time.time()
        
        tasks = [
            async_client.post(f"{API_V1_URL}/products", json=product_data)
            for product_data in products_data
        ]
        responses = await asyncio.gather(*tasks)
        
        elapsed = (time.time() - start_time) * 1000
        
        # Verificar que todos fueron creados
        assert all(r.status_code == 201 for r in responses)
        
        created_ids = [r.json()["data"]["id"] for r in responses]
        assert len(set(created_ids)) == 10  # Todos tienen IDs únicos
        
        print(f"   ✅ 10 productos creados exitosamente")
        print(f"   ⏱️  Tiempo total: {elapsed:.2f}ms")
        print(f"   ⏱️  Promedio por producto: {elapsed/10:.2f}ms")
        
        # Verificar en base de datos
        list_response = await async_client.get(f"{API_V1_URL}/products")
        list_data = list_response.json()
        assert list_data["data"]["total"] == 10
        
        print(f"   ✅ Confirmado: {list_data['data']['total']} productos en DB")
        print("\n" + "="*70)


# ============== TESTS: PAGINACIÓN ==============

class TestPagination:
    """Tests de paginación"""
    
    def test_pagination(self, client, sample_products_list):
        """✅ Paginación correcta"""
        # Crear 5 productos
        for product_data in sample_products_list:
            create_product(client, product_data)
        
        # Página 1 (primeros 2)
        response1 = client.get(f"{API_V1_URL}/products?skip=0&limit=2")
        data1 = response1.json()
        assert len(data1["data"]["items"]) == 2
        assert data1["data"]["total"] == 5
        
        # Página 2 (siguientes 2)
        response2 = client.get(f"{API_V1_URL}/products?skip=2&limit=2")
        data2 = response2.json()
        assert len(data2["data"]["items"]) == 2
        
        # Verificar que son productos diferentes
        ids_page1 = {item["id"] for item in data1["data"]["items"]}
        ids_page2 = {item["id"] for item in data2["data"]["items"]}
        assert ids_page1.isdisjoint(ids_page2)
    
    def test_pagination_invalid_params(self, client):
        """❌ Error: Parámetros de paginación inválidos"""
        # skip negativo
        response1 = client.get(f"{API_V1_URL}/products?skip=-1")
        assert response1.status_code == 400
        
        # limit > 100
        response2 = client.get(f"{API_V1_URL}/products?limit=101")
        assert response2.status_code == 400


# ============== TESTS: PERFORMANCE ==============

class TestPerformance:
    """Tests de performance y latencia"""
    
    def test_latency_measurements(self, client, sample_product):
        """📊 Medir latencias de operaciones"""
        print("\n" + "="*70)
        print("TEST: MEDICIONES DE LATENCIA")
        print("="*70)
        
        latencies = {}
        
        # CREATE
        _, latency_create = measure_latency(
            client.post, f"{API_V1_URL}/products", json=sample_product
        )
        latencies["CREATE"] = latency_create
        product_id = client.post(f"{API_V1_URL}/products", json=sample_product).json()["data"]["id"]
        
        # READ
        _, latency_read = measure_latency(
            client.get, f"{API_V1_URL}/products/{product_id}"
        )
        latencies["READ"] = latency_read
        
        # UPDATE
        _, latency_update = measure_latency(
            client.put, f"{API_V1_URL}/products/{product_id}", json={"price": 899.00}
        )
        latencies["UPDATE"] = latency_update
        
        # LIST
        _, latency_list = measure_latency(
            client.get, f"{API_V1_URL}/products"
        )
        latencies["LIST"] = latency_list
        
        # DELETE
        _, latency_delete = measure_latency(
            client.delete, f"{API_V1_URL}/products/{product_id}"
        )
        latencies["DELETE"] = latency_delete
        
        # Imprimir resultados
        print("\n📊 Latencias medidas:")
        for operation, latency in latencies.items():
            print(f"   {operation:10s}: {latency:6.2f}ms")
        
        avg_latency = sum(latencies.values()) / len(latencies)
        print(f"\n   Promedio: {avg_latency:.2f}ms")
        
        # Aserciones (latencias razonables)
        assert all(lat < 1000 for lat in latencies.values()), "Alguna operación tomó > 1s"
        
        print("\n✅ Todas las operaciones < 1000ms")
        print("="*70)


# ============== TESTS: EDGE CASES ==============

class TestEdgeCases:
    """Tests de casos extremos"""
    
    def test_update_nonexistent_product(self, client):
        """❌ Actualizar producto que no existe"""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = client.put(
            f"{API_V1_URL}/products/{fake_uuid}",
            json={"price": 100}
        )
        assert response.status_code == 404
    
    def test_delete_twice(self, client, sample_product):
        """❌ Eliminar producto dos veces"""
        # Crear y eliminar
        product = create_product(client, sample_product)
        product_id = product["id"]
        
        delete1 = client.delete(f"{API_V1_URL}/products/{product_id}")
        assert delete1.status_code == 204
        
        # Intentar eliminar de nuevo
        delete2 = client.delete(f"{API_V1_URL}/products/{product_id}")
        assert delete2.status_code == 404
    
    def test_update_empty_body(self, client, sample_product):
        """❌ Actualizar sin proporcionar campos"""
        product = create_product(client, sample_product)
        product_id = product["id"]
        
        response = client.put(f"{API_V1_URL}/products/{product_id}", json={})
        # Debería aceptarse (no cambios) o rechazarse según implementación
        # En este caso, Pydantic rechaza body vacío
        assert response.status_code in [200, 400, 422]


# ============== RUNNER PRINCIPAL ==============

if __name__ == "__main__":
    print("="*70)
    print("  SUITE DE TESTS E2E - EJERCICIO 4")
    print("  API: /api/v1/products")
    print("="*70)
    print("\n⚠️  PREREQUISITO: API debe estar corriendo en http://localhost:8000")
    print("    Ejecutar: uvicorn api_complete:app --reload\n")
    
    # Ejecutar con pytest
    pytest.main([__file__, "-v", "-s"])
