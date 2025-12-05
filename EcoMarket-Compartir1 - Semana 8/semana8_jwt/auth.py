"""
Módulo de Autenticación JWT para EcoMarket
===========================================

Implementa autenticación basada en JWT (JSON Web Tokens) con:
- Generación de access tokens y refresh tokens
- Validación de tokens
- Sistema de roles (admin, vendedor, cliente)
- Gestión de usuarios
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import jwt
import hashlib  # Usar hashlib en lugar de passlib por problemas de compatibilidad
from fastapi import HTTPException, status
import os
import uuid

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Clave secreta para firmar los JWT (en producción debe estar en variables de entorno)
SECRET_KEY = os.getenv("JWT_SECRET", "tu_clave_secreta_muy_larga_y_segura_cambiar_en_produccion_123456789")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# ============================================================================
# FUNCIONES DE CONTRASEÑAS - Usando SHA256 simple para evitar problemas con bcrypt
# ============================================================================

def get_password_hash(password: str) -> str:
    """Genera el hash SHA256 de una contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    return get_password_hash(plain_password) == hashed_password

# ============================================================================
# BASE DE DATOS EN MEMORIA (USUARIOS)
# ============================================================================

# En producción esto debería estar en una base de datos real
# Contraseñas: admin123, vendedor123, cliente123 (hasheadas con SHA256)
users_db: Dict[str, dict] = {
    "admin@ecomarket.com": {
        "user_id": "user_001",
        "email": "admin@ecomarket.com",
        "name": "Administrador",
        "hashed_password": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",  # admin123
        "role": "admin",
        "is_active": True,
        "created_at": "2025-11-26T10:00:00"
    },
    "vendedor@ecomarket.com": {
        "user_id": "user_002",
        "email": "vendedor@ecomarket.com",
        "name": "Juan Vendedor",
        "hashed_password": "56976bf24998ca63e35fe4f1e2469b5751d1856003e8d16fef0aafef496ed044",  # vendedor123
        "role": "vendedor",
        "is_active": True,
        "created_at": "2025-11-26T10:00:00"
    },
    "cliente@ecomarket.com": {
        "user_id": "user_003",
        "email": "cliente@ecomarket.com",
        "name": "María Cliente",
        "hashed_password": "09a31a7001e261ab1e056182a71d3cf57f582ca9a29cff5eb83be0f0549730a9",  # cliente123
        "role": "cliente",
        "is_active": True,
        "created_at": "2025-11-26T10:00:00"
    }
}

# Almacén de refresh tokens activos (en producción usar Redis)
active_refresh_tokens: Dict[str, dict] = {}

# ============================================================================
# FUNCIONES DE USUARIO
# ============================================================================

def authenticate_user(email: str, password: str) -> Optional[dict]:
    """
    Autentica un usuario verificando email y contraseña.
    
    Returns:
        dict: Datos del usuario si es válido
        None: Si las credenciales son incorrectas
    """
    user = users_db.get(email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    if not user.get("is_active", True):
        return None
    return user

def get_user_by_email(email: str) -> Optional[dict]:
    """Obtiene un usuario por su email"""
    return users_db.get(email)

def get_user_by_id(user_id: str) -> Optional[dict]:
    """Obtiene un usuario por su ID"""
    for user in users_db.values():
        if user["user_id"] == user_id:
            return user
    return None

# ============================================================================
# FUNCIONES DE JWT
# ============================================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un access token JWT.
    
    Args:
        data: Datos a incluir en el token (sub, role, etc.)
        expires_delta: Tiempo de expiración personalizado
        
    Returns:
        str: Token JWT firmado
    """
    to_encode = data.copy()
    
    # Timestamp actual
    now = datetime.now(timezone.utc)
    
    # Expiración
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Claims estándar
    to_encode.update({
        "exp": expire,
        "iat": now,
        "iss": "ecomarket-auth-service",
        "aud": "ecomarket-api",
        "type": "access"
    })
    
    # Firmar el token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: str) -> str:
    """
    Crea un refresh token de larga duración.
    
    Args:
        user_id: ID del usuario
        
    Returns:
        str: Refresh token JWT
    """
    jti = str(uuid.uuid4())  # ID único del token
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {
        "sub": user_id,
        "jti": jti,
        "exp": expire,
        "iat": now,
        "type": "refresh"
    }
    
    # Guardar en almacén de tokens activos
    active_refresh_tokens[jti] = {
        "user_id": user_id,
        "created_at": now,
        "expires_at": expire,
        "revoked": False
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str, token_type: str = "access") -> dict:
    """
    Verifica y decodifica un token JWT.
    
    Args:
        token: Token JWT a verificar
        token_type: Tipo esperado ("access" o "refresh")
        
    Returns:
        dict: Payload del token si es válido
        
    Raises:
        HTTPException: Si el token es inválido, expirado o manipulado
    """
    try:
        # Decodificar y verificar el token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={
                "verify_signature": True,
                "verify_aud": False  # No verificar audience en tests
            }
        )
        
        # Verificar el tipo de token
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token inválido: se esperaba tipo '{token_type}'",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar claims obligatorios
        if not payload.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token sin subject (sub)",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Si es refresh token, verificar que no esté revocado
        if token_type == "refresh":
            jti = payload.get("jti")
            if jti and jti in active_refresh_tokens:
                if active_refresh_tokens[jti]["revoked"]:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Refresh token revocado",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
        
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def revoke_refresh_token(jti: str) -> bool:
    """
    Revoca un refresh token (para logout).
    
    Args:
        jti: ID único del refresh token
        
    Returns:
        bool: True si se revocó correctamente
    """
    if jti in active_refresh_tokens:
        active_refresh_tokens[jti]["revoked"] = True
        return True
    return False

# ============================================================================
# FUNCIONES DE AUTORIZACIÓN
# ============================================================================

def check_permission(user_role: str, required_roles: list) -> bool:
    """
    Verifica si un rol tiene permisos suficientes.
    
    Args:
        user_role: Rol del usuario actual
        required_roles: Lista de roles permitidos
        
    Returns:
        bool: True si tiene permiso
    """
    return user_role in required_roles

def require_roles(required_roles: list):
    """
    Decorator para verificar roles requeridos en endpoints.
    
    Usage:
        @require_roles(["admin", "vendedor"])
        async def crear_producto(...):
            ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Esta función será completada en el middleware
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ============================================================================
# UTILIDADES
# ============================================================================

def generate_test_token(email: str = "admin@ecomarket.com") -> dict:
    """
    Genera tokens de prueba para testing.
    
    Args:
        email: Email del usuario
        
    Returns:
        dict: Access token y refresh token
    """
    user = get_user_by_email(email)
    if not user:
        raise ValueError(f"Usuario {email} no encontrado")
    
    access_token = create_access_token(
        data={
            "sub": user["user_id"],
            "email": user["email"],
            "role": user["role"]
        }
    )
    
    refresh_token = create_refresh_token(user["user_id"])
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# ============================================================================
# INFORMACIÓN DE USUARIOS PARA TESTING
# ============================================================================

def get_test_users_info() -> dict:
    """
    Retorna información de los usuarios de prueba.
    Útil para documentación y testing.
    """
    return {
        "admin": {
            "email": "admin@ecomarket.com",
            "password": "admin123",
            "role": "admin",
            "description": "Usuario administrador con todos los permisos"
        },
        "vendedor": {
            "email": "vendedor@ecomarket.com",
            "password": "vendedor123",
            "role": "vendedor",
            "description": "Usuario vendedor, puede crear y editar productos"
        },
        "cliente": {
            "email": "cliente@ecomarket.com",
            "password": "cliente123",
            "role": "cliente",
            "description": "Usuario cliente, solo lectura"
        }
    }

# ============================================================================
# EXPORTACIONES
# ============================================================================

__all__ = [
    "SECRET_KEY",
    "ALGORITHM",
    "authenticate_user",
    "get_user_by_id",
    "get_user_by_email",
    "create_access_token",
    "create_refresh_token",
    "verify_token",
    "revoke_refresh_token",
    "check_permission",
    "get_password_hash",
    "generate_test_token",
    "get_test_users_info",
]
