"""
Endpoints de autenticación JWT para integrar en main.py
========================================================

Este archivo contiene todos los endpoints relacionados con autenticación:
- /api/auth/login: Login con email y contraseña
- /api/auth/refresh: Renovar access token con refresh token
- /api/auth/logout: Cerrar sesión (revocar refresh token)
- /api/auth/me: Obtener información del usuario actual
- /api/auth/test-users: Obtener usuarios de prueba
- /api/auth/info: Información del sistema de autenticación
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports absolutos
sys.path.insert(0, str(Path(__file__).parent.parent))

from semana8_jwt import auth, models, middleware

# Router para agrupar endpoints
router = APIRouter(prefix="/api/auth", tags=["Autenticación JWT"])

# ============================================================================
# ENDPOINT: LOGIN
# ============================================================================

@router.post(
    "/login",
    response_model=models.TokenResponse,
    summary="Iniciar sesión",
    description="Autentica un usuario con email y contraseña, retorna tokens JWT",
)
async def login(credentials: models.LoginCredentials):
    """
    **Login con JWT**
    
    Autentica un usuario y genera tokens de acceso:
    - **Access Token**: Válido por 30 minutos, para acceder a la API
    - **Refresh Token**: Válido por 7 días, para renovar el access token
    
    **Usuarios de prueba:**
    - admin@ecomarket.com / admin123 (rol: admin)
    - vendedor@ecomarket.com / vendedor123 (rol: vendedor)
    - cliente@ecomarket.com / cliente123 (rol: cliente)
    
    **Ejemplo de respuesta:**
    ```json
    {
        "access_token": "eyJhbGci...",
        "refresh_token": "eyJhbGci...",
        "token_type": "bearer",
        "expires_in": 1800
    }
    ```
    
    **Cómo usar el token:**
    ```
    Authorization: Bearer <access_token>
    ```
    """
    # Autenticar usuario
    user = auth.authenticate_user(credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear access token
    access_token = auth.create_access_token(
        data={
            "sub": user["user_id"],
            "email": user["email"],
            "role": user["role"]
        }
    )
    
    # Crear refresh token
    refresh_token = auth.create_refresh_token(user["user_id"])
    
    return models.TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "email": user["email"],
            "role": user["role"],
            "nombre": user.get("nombre", user["email"].split("@")[0].capitalize())
        }
    )

# ============================================================================
# ENDPOINT: REFRESH TOKEN
# ============================================================================

@router.post(
    "/refresh",
    response_model=models.TokenResponse,
    summary="Renovar access token",
    description="Usa un refresh token para obtener un nuevo access token",
)
async def refresh_token(request: models.RefreshTokenRequest):
    """
    **Renovar Access Token**
    
    Usa un refresh token válido para obtener un nuevo access token
    sin necesidad de volver a iniciar sesión.
    
    El refresh token es válido por 7 días.
    """
    try:
        # Verificar refresh token
        payload = auth.verify_token(request.refresh_token, token_type="refresh")
        user_id = payload.get("sub")
        
        # Obtener usuario
        user = auth.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado"
            )
        
        # Crear nuevo access token
        new_access_token = auth.create_access_token(
            data={
                "sub": user["user_id"],
                "email": user["email"],
                "role": user["role"]
            }
        )
        
        return models.TokenResponse(
            access_token=new_access_token,
            refresh_token=request.refresh_token,  # Mismo refresh token
            token_type="bearer",
            expires_in=auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Refresh token inválido: {str(e)}"
        )

# ============================================================================
# ENDPOINT: LOGOUT
# ============================================================================

@router.post(
    "/logout",
    response_model=models.MessageResponse,
    summary="Cerrar sesión",
    description="Revoca un refresh token para cerrar sesión",
)
async def logout(request: models.LogoutRequest):
    """
    **Cerrar Sesión**
    
    Revoca un refresh token, impidiendo que pueda ser usado para
    generar nuevos access tokens.
    
    El access token actual seguirá siendo válido hasta que expire.
    """
    try:
        # Verificar y extraer JTI del refresh token
        payload = auth.verify_token(request.refresh_token, token_type="refresh")
        jti = payload.get("jti")
        
        if not jti:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token sin identificador único"
            )
        
        # Revocar el refresh token
        revoked = auth.revoke_refresh_token(jti)
        
        if not revoked:
            return models.MessageResponse(
                message="Token ya estaba revocado o no existe",
                detail="El token no se encontró en el sistema"
            )
        
        return models.MessageResponse(
            message="Sesión cerrada exitosamente",
            detail="El refresh token ha sido revocado"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al cerrar sesión: {str(e)}"
        )

# ============================================================================
# ENDPOINT: USUARIO ACTUAL
# ============================================================================

@router.get(
    "/me",
    response_model=models.UserResponse,
    summary="Obtener usuario actual",
    description="Retorna información del usuario autenticado",
)
async def get_current_user_info(
    user: dict = Depends(middleware.get_current_user)
):
    """
    **Mi Perfil**
    
    Obtiene la información del usuario autenticado actual.
    
    **Requiere autenticación**: Debes incluir el access token en el header.
    ```
    Authorization: Bearer <access_token>
    ```
    """
    return models.UserResponse(
        user_id=user["user_id"],
        email=user["email"],
        name=user["name"],
        role=user["role"],
        is_active=user["is_active"],
        created_at=user["created_at"]
    )

# ============================================================================
# ENDPOINT: INFORMACIÓN DEL SISTEMA
# ============================================================================

@router.get(
    "/info",
    response_model=models.AuthInfo,
    summary="Información del sistema de autenticación",
    description="Retorna configuración y detalles del sistema JWT",
)
async def get_auth_info():
    """
    **Información del Sistema**
    
    Obtiene información sobre la configuración del sistema de autenticación:
    - Algoritmo de firma JWT
    - Tiempos de expiración
    - Roles disponibles
    """
    return models.AuthInfo(
        algorithm=auth.ALGORITHM,
        access_token_expire_minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_days=auth.REFRESH_TOKEN_EXPIRE_DAYS,
        available_roles=["admin", "vendedor", "cliente"]
    )

# ============================================================================
# ENDPOINT: USUARIOS DE PRUEBA
# ============================================================================

@router.get(
    "/test-users",
    summary="Usuarios de prueba",
    description="Retorna información de los usuarios de prueba disponibles",
)
async def get_test_users():
    """
    **Usuarios de Prueba**
    
    Lista de usuarios de prueba para testing de la API:
    
    - **Admin**: admin@ecomarket.com / admin123
    - **Vendedor**: vendedor@ecomarket.com / vendedor123
    - **Cliente**: cliente@ecomarket.com / cliente123
    
    Usa estos usuarios para probar diferentes niveles de acceso.
    """
    return auth.get_test_users_info()

# ============================================================================
# ENDPOINT DE PRUEBA: GENERAR TOKEN
# ============================================================================

@router.post(
    "/generate-test-token",
    response_model=models.TokenResponse,
    summary="Generar token de prueba (solo para desarrollo)",
    description="Genera tokens de prueba sin verificar contraseña",
)
async def generate_test_token_endpoint(email: str = "admin@ecomarket.com"):
    """
    **⚠️ Solo para Desarrollo**
    
    Genera tokens de prueba sin verificar contraseña.
    Este endpoint debería estar deshabilitado en producción.
    """
    try:
        tokens = auth.generate_test_token(email)
        return models.TokenResponse(**tokens)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# ============================================================================
# EXPORTAR ROUTER
# ============================================================================

__all__ = ["router"]
