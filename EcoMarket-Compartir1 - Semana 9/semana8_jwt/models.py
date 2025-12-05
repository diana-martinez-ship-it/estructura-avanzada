"""
Modelos Pydantic para Autenticación JWT
========================================

Define las estructuras de datos para:
- Credenciales de login
- Tokens de respuesta
- Usuarios
- Payloads de JWT
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ============================================================================
# MODELOS DE AUTENTICACIÓN
# ============================================================================

class LoginCredentials(BaseModel):
    """
    Credenciales para login.
    
    Example:
        {
            "email": "admin@ecomarket.com",
            "password": "admin123"
        }
    """
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "admin@ecomarket.com",
                    "password": "admin123"
                }
            ]
        }
    }

class TokenResponse(BaseModel):
    """
    Respuesta de autenticación exitosa.
    
    Example:
        {
            "access_token": "eyJhbGci...",
            "refresh_token": "eyJhbGci...",
            "token_type": "bearer",
            "expires_in": 1800,
            "user": {
                "email": "admin@ecomarket.com",
                "role": "admin",
                "nombre": "Administrador"
            }
        }
    """
    access_token: str = Field(..., description="Token de acceso JWT")
    refresh_token: str = Field(..., description="Token de refresco para renovar el access token")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(default=1800, description="Tiempo de expiración en segundos (30 min)")
    user: dict = Field(..., description="Información del usuario autenticado")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzAwMSIsImVtYWlsIjoiYWRtaW5AZWNvbWFya2V0LmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTczMjYyNjAwMCwiaWF0IjoxNzMyNjI0MjAwLCJpc3MiOiJlY29tYXJrZXQtYXV0aC1zZXJ2aWNlIiwiYXVkIjoiZWNvbWFya2V0LWFwaSIsInR5cGUiOiJhY2Nlc3MifQ.signature",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzAwMSIsImp0aSI6IjEyMzQ1Njc4LTkwYWItY2RlZi0xMjM0LTU2Nzg5MGFiY2RlZiIsImV4cCI6MTczMzIzMDAwMCwiaWF0IjoxNzMyNjI0MjAwLCJ0eXBlIjoicmVmcmVzaCJ9.signature",
                    "token_type": "bearer",
                    "expires_in": 1800
                }
            ]
        }
    }

class RefreshTokenRequest(BaseModel):
    """
    Solicitud para refrescar un access token.
    
    Example:
        {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    """
    refresh_token: str = Field(..., description="Refresh token válido")

class LogoutRequest(BaseModel):
    """
    Solicitud para cerrar sesión (revocar refresh token).
    
    Example:
        {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
    """
    refresh_token: str = Field(..., description="Refresh token a revocar")

# ============================================================================
# MODELOS DE USUARIO
# ============================================================================

class UserBase(BaseModel):
    """Modelo base de usuario"""
    email: EmailStr = Field(..., description="Email del usuario")
    name: str = Field(..., min_length=1, max_length=100, description="Nombre completo")
    role: str = Field(..., description="Rol del usuario: admin, vendedor, cliente")
    is_active: bool = Field(default=True, description="Usuario activo")

class UserCreate(UserBase):
    """Modelo para crear un nuevo usuario"""
    password: str = Field(..., min_length=6, description="Contraseña en texto plano")

class UserInDB(UserBase):
    """Modelo de usuario en base de datos"""
    user_id: str = Field(..., description="ID único del usuario")
    hashed_password: str = Field(..., description="Contraseña hasheada")
    created_at: str = Field(..., description="Fecha de creación")

class UserResponse(UserBase):
    """Modelo de usuario para respuestas (sin contraseña)"""
    user_id: str = Field(..., description="ID único del usuario")
    created_at: str = Field(..., description="Fecha de creación")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "user_001",
                    "email": "admin@ecomarket.com",
                    "name": "Administrador",
                    "role": "admin",
                    "is_active": True,
                    "created_at": "2025-11-26T10:00:00"
                }
            ]
        }
    }

# ============================================================================
# MODELOS DE JWT
# ============================================================================

class TokenPayload(BaseModel):
    """
    Payload decodificado de un JWT.
    
    Claims estándar:
    - sub: subject (user_id)
    - exp: expiration time
    - iat: issued at
    - iss: issuer
    - aud: audience
    - type: access o refresh
    """
    sub: str = Field(..., description="Subject: ID del usuario")
    email: Optional[str] = Field(None, description="Email del usuario")
    role: Optional[str] = Field(None, description="Rol del usuario")
    exp: int = Field(..., description="Expiration: timestamp de expiración")
    iat: int = Field(..., description="Issued At: timestamp de emisión")
    iss: Optional[str] = Field(None, description="Issuer: emisor del token")
    aud: Optional[str] = Field(None, description="Audience: audiencia del token")
    type: str = Field(..., description="Tipo de token: access o refresh")
    jti: Optional[str] = Field(None, description="JWT ID: identificador único (para refresh tokens)")

# ============================================================================
# MODELOS DE RESPUESTA
# ============================================================================

class MessageResponse(BaseModel):
    """Respuesta genérica con mensaje"""
    message: str = Field(..., description="Mensaje de la operación")
    detail: Optional[str] = Field(None, description="Detalles adicionales")

class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""
    detail: str = Field(..., description="Descripción del error")
    error_code: Optional[str] = Field(None, description="Código de error")

# ============================================================================
# MODELOS DE INFORMACIÓN DEL SISTEMA
# ============================================================================

class AuthInfo(BaseModel):
    """Información sobre el sistema de autenticación"""
    algorithm: str = Field(..., description="Algoritmo de firma JWT")
    access_token_expire_minutes: int = Field(..., description="Minutos de validez del access token")
    refresh_token_expire_days: int = Field(..., description="Días de validez del refresh token")
    available_roles: list[str] = Field(..., description="Roles disponibles en el sistema")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "algorithm": "HS256",
                    "access_token_expire_minutes": 30,
                    "refresh_token_expire_days": 7,
                    "available_roles": ["admin", "vendedor", "cliente"]
                }
            ]
        }
    }

class TestUsersInfo(BaseModel):
    """Información de usuarios de prueba"""
    email: str
    password: str
    role: str
    description: str

# ============================================================================
# EXPORTACIONES
# ============================================================================

__all__ = [
    "LoginCredentials",
    "TokenResponse",
    "RefreshTokenRequest",
    "LogoutRequest",
    "UserBase",
    "UserCreate",
    "UserInDB",
    "UserResponse",
    "TokenPayload",
    "MessageResponse",
    "ErrorResponse",
    "AuthInfo",
    "TestUsersInfo",
]
