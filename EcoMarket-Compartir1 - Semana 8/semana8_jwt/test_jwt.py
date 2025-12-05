"""
Tests para Sistema JWT - Semana 8
==================================

Tests completos para autenticación y autorización JWT.
"""

import pytest
from fastapi.testclient import TestClient
import jwt
from datetime import datetime, timedelta, timezone
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from semana8_jwt import auth, models

# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def valid_credentials():
    """Credenciales válidas de admin"""
    return {
        "email": "admin@ecomarket.com",
        "password": "admin123"
    }

@pytest.fixture
def vendedor_credentials():
    """Credenciales válidas de vendedor"""
    return {
        "email": "vendedor@ecomarket.com",
        "password": "vendedor123"
    }

@pytest.fixture
def cliente_credentials():
    """Credenciales válidas de cliente"""
    return {
        "email": "cliente@ecomarket.com",
        "password": "cliente123"
    }

@pytest.fixture
def valid_token():
    """Token JWT válido de admin"""
    return auth.create_access_token(
        data={
            "sub": "user_001",
            "email": "admin@ecomarket.com",
            "role": "admin"
        }
    )

@pytest.fixture
def expired_token():
    """Token JWT expirado"""
    return auth.create_access_token(
        data={
            "sub": "user_001",
            "email": "admin@ecomarket.com",
            "role": "admin"
        },
        expires_delta=timedelta(seconds=-1)  # Expirado hace 1 segundo
    )

@pytest.fixture
def manipulated_token(valid_token):
    """Token JWT manipulado (firma inválida)"""
    # Cambiar un carácter del token para invalidar la firma
    return valid_token[:-5] + "xxxxx"

# ============================================================================
# TESTS DE AUTENTICACIÓN
# ============================================================================

class TestAuthentication:
    """Tests para el proceso de autenticación"""
    
    def test_authenticate_user_success(self, valid_credentials):
        """Test: Autenticación exitosa con credenciales válidas"""
        user = auth.authenticate_user(
            valid_credentials["email"],
            valid_credentials["password"]
        )
        
        assert user is not None
        assert user["email"] == valid_credentials["email"]
        assert user["role"] == "admin"
        assert user["is_active"] is True
    
    def test_authenticate_user_wrong_password(self):
        """Test: Autenticación fallida con contraseña incorrecta"""
        user = auth.authenticate_user(
            "admin@ecomarket.com",
            "wrongpassword"
        )
        
        assert user is None
    
    def test_authenticate_user_nonexistent(self):
        """Test: Autenticación fallida con usuario inexistente"""
        user = auth.authenticate_user(
            "noexiste@ecomarket.com",
            "password123"
        )
        
        assert user is None
    
    def test_get_user_by_email(self):
        """Test: Obtener usuario por email"""
        user = auth.get_user_by_email("admin@ecomarket.com")
        
        assert user is not None
        assert user["user_id"] == "user_001"
        assert user["role"] == "admin"
    
    def test_get_user_by_id(self):
        """Test: Obtener usuario por ID"""
        user = auth.get_user_by_id("user_001")
        
        assert user is not None
        assert user["email"] == "admin@ecomarket.com"
        assert user["role"] == "admin"

# ============================================================================
# TESTS DE TOKENS JWT
# ============================================================================

class TestJWTTokens:
    """Tests para creación y validación de tokens JWT"""
    
    def test_create_access_token(self):
        """Test: Crear access token válido"""
        token = auth.create_access_token(
            data={"sub": "user_001", "email": "admin@ecomarket.com", "role": "admin"}
        )
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 50  # JWT típico es largo
    
    def test_verify_valid_token(self, valid_token):
        """Test: Verificar token válido"""
        payload = auth.verify_token(valid_token, token_type="access")
        
        assert payload is not None
        assert payload["sub"] == "user_001"
        assert payload["email"] == "admin@ecomarket.com"
        assert payload["role"] == "admin"
        assert payload["type"] == "access"
        assert payload["iss"] == "ecomarket-auth-service"
        assert payload["aud"] == "ecomarket-api"
    
    def test_verify_expired_token(self, expired_token):
        """Test: Verificar token expirado"""
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            auth.verify_token(expired_token, token_type="access")
        
        assert exc_info.value.status_code == 401
        assert "expirado" in exc_info.value.detail.lower()
    
    def test_verify_manipulated_token(self, manipulated_token):
        """Test: Verificar token manipulado"""
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            auth.verify_token(manipulated_token, token_type="access")
        
        assert exc_info.value.status_code == 401
        assert "inválido" in exc_info.value.detail.lower()
    
    def test_verify_wrong_token_type(self):
        """Test: Verificar token con tipo incorrecto"""
        from fastapi import HTTPException
        
        # Crear un refresh token
        refresh_token = auth.create_refresh_token("user_001")
        
        # Intentar verificarlo como access token
        with pytest.raises(HTTPException) as exc_info:
            auth.verify_token(refresh_token, token_type="access")
        
        assert exc_info.value.status_code == 401
        assert "tipo" in exc_info.value.detail.lower()
    
    def test_create_refresh_token(self):
        """Test: Crear refresh token"""
        refresh_token = auth.create_refresh_token("user_001")
        
        assert refresh_token is not None
        assert isinstance(refresh_token, str)
        
        # Verificar el payload
        payload = auth.verify_token(refresh_token, token_type="refresh")
        assert payload["sub"] == "user_001"
        assert payload["type"] == "refresh"
        assert "jti" in payload
    
    def test_revoke_refresh_token(self):
        """Test: Revocar refresh token"""
        from fastapi import HTTPException
        
        # Crear y verificar que funciona
        refresh_token = auth.create_refresh_token("user_001")
        payload = auth.verify_token(refresh_token, token_type="refresh")
        jti = payload["jti"]
        
        # Revocar
        result = auth.revoke_refresh_token(jti)
        assert result is True
        
        # Verificar que ya no funciona
        with pytest.raises(HTTPException) as exc_info:
            auth.verify_token(refresh_token, token_type="refresh")
        
        assert exc_info.value.status_code == 401
        assert "revocado" in exc_info.value.detail.lower()

# ============================================================================
# TESTS DE ROLES Y PERMISOS
# ============================================================================

class TestRolesAndPermissions:
    """Tests para el sistema de roles y permisos"""
    
    def test_check_permission_admin(self):
        """Test: Admin tiene permisos de admin"""
        result = auth.check_permission("admin", ["admin"])
        assert result is True
    
    def test_check_permission_admin_multiple_roles(self):
        """Test: Admin tiene permisos cuando se aceptan múltiples roles"""
        result = auth.check_permission("admin", ["admin", "vendedor"])
        assert result is True
    
    def test_check_permission_vendedor_no_admin(self):
        """Test: Vendedor NO tiene permisos de admin"""
        result = auth.check_permission("vendedor", ["admin"])
        assert result is False
    
    def test_check_permission_cliente_restricted(self):
        """Test: Cliente NO tiene permisos de admin ni vendedor"""
        result_admin = auth.check_permission("cliente", ["admin"])
        result_vendedor = auth.check_permission("cliente", ["vendedor"])
        
        assert result_admin is False
        assert result_vendedor is False
    
    def test_token_contains_role_admin(self, valid_credentials):
        """Test: Token de admin contiene el rol correcto"""
        user = auth.authenticate_user(
            valid_credentials["email"],
            valid_credentials["password"]
        )
        token = auth.create_access_token(
            data={"sub": user["user_id"], "role": user["role"]}
        )
        payload = auth.verify_token(token)
        
        assert payload["role"] == "admin"
    
    def test_token_contains_role_vendedor(self, vendedor_credentials):
        """Test: Token de vendedor contiene el rol correcto"""
        user = auth.authenticate_user(
            vendedor_credentials["email"],
            vendedor_credentials["password"]
        )
        token = auth.create_access_token(
            data={"sub": user["user_id"], "role": user["role"]}
        )
        payload = auth.verify_token(token)
        
        assert payload["role"] == "vendedor"

# ============================================================================
# TESTS DE MODELOS PYDANTIC
# ============================================================================

class TestModels:
    """Tests para los modelos Pydantic"""
    
    def test_login_credentials_valid(self):
        """Test: Modelo LoginCredentials con datos válidos"""
        creds = models.LoginCredentials(
            email="test@ecomarket.com",
            password="password123"
        )
        
        assert creds.email == "test@ecomarket.com"
        assert creds.password == "password123"
    
    def test_login_credentials_invalid_email(self):
        """Test: Modelo LoginCredentials rechaza email inválido"""
        with pytest.raises(Exception):  # ValidationError
            models.LoginCredentials(
                email="not-an-email",
                password="password123"
            )
    
    def test_token_response_structure(self):
        """Test: Estructura de TokenResponse"""
        response = models.TokenResponse(
            access_token="access_token_here",
            refresh_token="refresh_token_here",
            token_type="bearer",
            expires_in=1800
        )
        
        assert response.access_token == "access_token_here"
        assert response.refresh_token == "refresh_token_here"
        assert response.token_type == "bearer"
        assert response.expires_in == 1800
    
    def test_user_response_structure(self):
        """Test: Estructura de UserResponse"""
        user = models.UserResponse(
            user_id="user_001",
            email="admin@ecomarket.com",
            name="Administrador",
            role="admin",
            is_active=True,
            created_at="2025-11-26T10:00:00"
        )
        
        assert user.user_id == "user_001"
        assert user.role == "admin"
        assert user.is_active is True

# ============================================================================
# TESTS DE SEGURIDAD
# ============================================================================

class TestSecurity:
    """Tests de seguridad del sistema JWT"""
    
    def test_password_hashing(self):
        """Test: Las contraseñas se hashean correctamente"""
        password = "mi_contraseña_segura"
        hashed = auth.get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 50  # bcrypt hash es largo
        assert auth.verify_password(password, hashed) is True
    
    def test_different_passwords_different_hashes(self):
        """Test: Misma contraseña genera hashes diferentes (salt)"""
        password = "mi_contraseña"
        hash1 = auth.get_password_hash(password)
        hash2 = auth.get_password_hash(password)
        
        assert hash1 != hash2  # Salt aleatorio
        assert auth.verify_password(password, hash1) is True
        assert auth.verify_password(password, hash2) is True
    
    def test_token_expiration(self):
        """Test: Token expira después del tiempo configurado"""
        # Crear token con expiración de 1 segundo
        token = auth.create_access_token(
            data={"sub": "user_001"},
            expires_delta=timedelta(seconds=1)
        )
        
        # Verificar que funciona inmediatamente
        payload = auth.verify_token(token)
        assert payload["sub"] == "user_001"
        
        # Esperar 2 segundos
        import time
        time.sleep(2)
        
        # Verificar que ahora está expirado
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            auth.verify_token(token)
        
        assert exc_info.value.status_code == 401
    
    def test_token_cannot_be_modified(self, valid_token):
        """Test: Token no puede ser modificado sin invalidar firma"""
        from fastapi import HTTPException
        
        # Decodificar sin verificar
        payload = jwt.decode(valid_token, options={"verify_signature": False})
        
        # Intentar cambiar el rol
        payload["role"] = "super_admin"
        
        # Crear nuevo token con el payload modificado (sin la clave correcta)
        modified_token = jwt.encode(payload, "clave_incorrecta", algorithm="HS256")
        
        # Verificar que falla la validación
        with pytest.raises(HTTPException):
            auth.verify_token(modified_token)

# ============================================================================
# TESTS DE INTEGRACIÓN
# ============================================================================

class TestIntegration:
    """Tests de integración del flujo completo"""
    
    def test_full_authentication_flow(self, valid_credentials):
        """Test: Flujo completo de autenticación"""
        # 1. Autenticar usuario
        user = auth.authenticate_user(
            valid_credentials["email"],
            valid_credentials["password"]
        )
        assert user is not None
        
        # 2. Crear access token
        access_token = auth.create_access_token(
            data={
                "sub": user["user_id"],
                "email": user["email"],
                "role": user["role"]
            }
        )
        assert access_token is not None
        
        # 3. Crear refresh token
        refresh_token = auth.create_refresh_token(user["user_id"])
        assert refresh_token is not None
        
        # 4. Verificar access token
        payload = auth.verify_token(access_token)
        assert payload["sub"] == user["user_id"]
        assert payload["role"] == user["role"]
        
        # 5. Verificar refresh token
        refresh_payload = auth.verify_token(refresh_token, token_type="refresh")
        assert refresh_payload["sub"] == user["user_id"]
    
    def test_refresh_token_flow(self):
        """Test: Flujo de renovación de token"""
        user = auth.get_user_by_email("admin@ecomarket.com")
        
        # 1. Crear refresh token
        refresh_token = auth.create_refresh_token(user["user_id"])
        
        # 2. Verificar refresh token
        payload = auth.verify_token(refresh_token, token_type="refresh")
        assert payload["sub"] == user["user_id"]
        
        # 3. Usar refresh token para crear nuevo access token
        new_access_token = auth.create_access_token(
            data={
                "sub": payload["sub"],
                "email": user["email"],
                "role": user["role"]
            }
        )
        
        # 4. Verificar nuevo access token
        new_payload = auth.verify_token(new_access_token)
        assert new_payload["sub"] == user["user_id"]

# ============================================================================
# TESTS DE UTILITIES
# ============================================================================

class TestUtilities:
    """Tests para funciones utilitarias"""
    
    def test_generate_test_token(self):
        """Test: Generar token de prueba"""
        tokens = auth.generate_test_token("admin@ecomarket.com")
        
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert "token_type" in tokens
        assert tokens["token_type"] == "bearer"
    
    def test_get_test_users_info(self):
        """Test: Obtener información de usuarios de prueba"""
        info = auth.get_test_users_info()
        
        assert "admin" in info
        assert "vendedor" in info
        assert "cliente" in info
        
        assert info["admin"]["email"] == "admin@ecomarket.com"
        assert info["admin"]["password"] == "admin123"
        assert info["admin"]["role"] == "admin"

# ============================================================================
# EJECUTAR TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
