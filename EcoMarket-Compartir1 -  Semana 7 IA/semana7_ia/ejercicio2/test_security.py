"""
Suite de Pruebas - Ejercicio 2: Autenticación y Rate Limiting
6 casos: 3 exitosos + 3 fallidos
"""
import pytest
from fastapi.testclient import TestClient
from api_secure import app, rate_limit_storage
import time

client = TestClient(app)


# ============== PRUEBAS EXITOSAS (✅) ==============

def test_1_login_exitoso():
    """✅ ÉXITO: Login con credenciales válidas"""
    print("\n" + "="*70)
    print("TEST 1: ✅ Login exitoso")
    print("="*70)
    
    response = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["error"] is None
    assert "accessToken" in data["data"]
    assert data["data"]["expiresIn"] == 900  # 15 min
    
    # Verificar cookie de refresh token
    assert "refresh_token" in response.cookies
    
    print("✅ Token JWT generado correctamente")
    print(f"✅ Access Token: {data['data']['accessToken'][:50]}...")
    print(f"✅ Cookie refresh_token configurada")
    
    return data["data"]["accessToken"]


def test_2_acceso_ruta_protegida_con_token():
    """✅ ÉXITO: Acceso a ruta protegida con token válido"""
    print("\n" + "="*70)
    print("TEST 2: ✅ Acceso a ruta protegida con autenticación")
    print("="*70)
    
    # Primero login
    login_response = client.post("/api/v1/auth/login", json={
        "username": "user1",
        "password": "user123"
    })
    token = login_response.json()["data"]["accessToken"]
    
    # Acceder a ruta protegida
    response = client.get(
        "/api/v1/user/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["error"] is None
    assert data["data"]["username"] == "user1"
    assert data["data"]["role"] == "user"
    
    # Verificar headers
    assert "X-Correlation-ID" in response.headers
    assert "X-RateLimit-Limit-IP" in response.headers
    
    print("✅ Usuario autenticado correctamente")
    print(f"✅ Datos del perfil: {data['data']}")
    print(f"✅ Correlation ID: {response.headers['X-Correlation-ID']}")
    print(f"✅ Rate Limit IP: {response.headers['X-RateLimit-Remaining-IP']}/100")


def test_3_admin_accede_ruta_admin():
    """✅ ÉXITO: Usuario admin accede a ruta exclusiva de admin"""
    print("\n" + "="*70)
    print("TEST 3: ✅ Admin accede a ruta restringida")
    print("="*70)
    
    # Login como admin
    login_response = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    token = login_response.json()["data"]["accessToken"]
    
    # Acceder a ruta /admin/*
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["error"] is None
    assert "users" in data["data"]
    assert len(data["data"]["users"]) == 2  # admin + user1
    
    print("✅ Admin accedió exitosamente")
    print(f"✅ Usuarios listados: {len(data['data']['users'])}")
    print(f"✅ Requestor: {data['meta']['requestedBy']}")


# ============== PRUEBAS FALLIDAS (❌) ==============

def test_4_acceso_sin_token():
    """❌ FALLO: Intentar acceder sin token (401 UNAUTHENTICATED)"""
    print("\n" + "="*70)
    print("TEST 4: ❌ Acceso sin autenticación")
    print("="*70)
    
    response = client.get("/api/v1/user/profile")
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 401
    data = response.json()
    assert data["data"] is None
    assert data["error"]["code"] == "UNAUTHENTICATED"
    assert "autenticado" in data["error"]["msg"].lower()
    
    print("❌ Acceso denegado correctamente")
    print(f"❌ Código de error: {data['error']['code']}")
    print(f"❌ Mensaje: {data['error']['msg']}")


def test_5_user_intenta_acceder_ruta_admin():
    """❌ FALLO: Usuario normal intenta acceder a ruta de admin (403 FORBIDDEN)"""
    print("\n" + "="*70)
    print("TEST 5: ❌ Usuario sin permisos intenta ruta admin")
    print("="*70)
    
    # Login como user1 (rol: user)
    login_response = client.post("/api/v1/auth/login", json={
        "username": "user1",
        "password": "user123"
    })
    token = login_response.json()["data"]["accessToken"]
    
    # Intentar acceder a ruta admin
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 403
    data = response.json()
    assert data["data"] is None
    assert data["error"]["code"] == "FORBIDDEN"
    assert "admin" in data["error"]["msg"].lower()
    
    print("❌ Acceso prohibido correctamente")
    print(f"❌ Código de error: {data['error']['code']}")
    print(f"❌ Mensaje: {data['error']['msg']}")


def test_6_rate_limit_excedido():
    """❌ FALLO: Rate limit por IP excedido (429 RATE_LIMITED)"""
    print("\n" + "="*70)
    print("TEST 6: ❌ Rate limit excedido")
    print("="*70)
    
    # Limpiar rate limit storage para test limpio
    rate_limit_storage.clear()
    
    # Hacer 101 requests (límite es 100)
    print("Haciendo 101 requests...")
    
    responses = []
    for i in range(101):
        response = client.get("/")
        responses.append(response)
        
        if i % 25 == 0:
            print(f"  Request {i+1}/101...")
    
    # Verificar que los primeros 100 fueron exitosos
    for i in range(100):
        assert responses[i].status_code == 200
    
    # Verificar que el request 101 fue bloqueado
    last_response = responses[100]
    print(f"\nStatus del request 101: {last_response.status_code}")
    print(f"Response: {last_response.json()}")
    
    assert last_response.status_code == 429
    data = last_response.json()
    assert data["data"] is None
    assert data["error"]["code"] == "RATE_LIMITED"
    
    # Verificar headers de rate limit
    assert "X-RateLimit-Limit" in last_response.headers
    assert last_response.headers["X-RateLimit-Remaining"] == "0"
    assert "Retry-After" in last_response.headers
    
    print("❌ Rate limit aplicado correctamente")
    print(f"❌ Código de error: {data['error']['code']}")
    print(f"❌ Mensaje: {data['error']['msg']}")
    print(f"❌ Límite: {last_response.headers['X-RateLimit-Limit']}")
    print(f"❌ Restantes: {last_response.headers['X-RateLimit-Remaining']}")
    print(f"❌ Retry-After: {last_response.headers['Retry-After']}s")


# ============== RUNNER ==============

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  SUITE DE PRUEBAS - EJERCICIO 2")
    print("  Autenticación JWT + Rate Limiting + RBAC")
    print("="*70)
    
    # Pruebas exitosas
    print("\n" + "🟢 " + "="*68)
    print("  PRUEBAS EXITOSAS (3)")
    print("="*70)
    
    test_1_login_exitoso()
    time.sleep(0.1)
    
    test_2_acceso_ruta_protegida_con_token()
    time.sleep(0.1)
    
    test_3_admin_accede_ruta_admin()
    
    # Pruebas fallidas
    print("\n" + "🔴 " + "="*68)
    print("  PRUEBAS FALLIDAS (3)")
    print("="*70)
    
    test_4_acceso_sin_token()
    time.sleep(0.1)
    
    test_5_user_intenta_acceder_ruta_admin()
    time.sleep(0.1)
    
    test_6_rate_limit_excedido()
    
    # Resumen
    print("\n" + "="*70)
    print("  ✅ RESUMEN: 6/6 pruebas ejecutadas correctamente")
    print("  • 3 casos exitosos (200, 200, 200)")
    print("  • 3 casos de error (401, 403, 429)")
    print("="*70 + "\n")
