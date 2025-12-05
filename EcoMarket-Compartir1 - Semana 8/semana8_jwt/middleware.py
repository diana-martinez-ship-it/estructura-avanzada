"""
Middleware JWT para FastAPI
============================

Middleware que valida tokens JWT en cada request y protege endpoints.
"""

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List
import logging
from functools import wraps

from .auth import verify_token, get_user_by_id

# Configurar logger
logger = logging.getLogger(__name__)

# Security scheme para Bearer tokens
security = HTTPBearer(auto_error=False)

# ============================================================================
# EXCEPCIONES PERSONALIZADAS
# ============================================================================

class UnauthorizedException(HTTPException):
    """Excepción para errores de autenticación"""
    def __init__(self, detail: str = "No autenticado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class ForbiddenException(HTTPException):
    """Excepción para errores de autorización"""
    def __init__(self, detail: str = "No tienes permisos para realizar esta acción"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )

# ============================================================================
# DEPENDENCY PARA OBTENER TOKEN
# ============================================================================

async def get_current_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """
    Dependency que extrae el token JWT del header Authorization.
    
    Args:
        credentials: Credenciales del header Authorization
        
    Returns:
        str: Token JWT
        
    Raises:
        UnauthorizedException: Si no hay token
    """
    if not credentials:
        logger.warning("Intento de acceso sin token")
        raise UnauthorizedException("Token no proporcionado")
    
    return credentials.credentials

# ============================================================================
# DEPENDENCY PARA OBTENER USUARIO ACTUAL
# ============================================================================

async def get_current_user(token: str = Depends(get_current_token)) -> dict:
    """
    Dependency que valida el token y retorna el usuario actual.
    
    Args:
        token: Token JWT del usuario
        
    Returns:
        dict: Datos del usuario actual
        
    Raises:
        UnauthorizedException: Si el token es inválido
    """
    try:
        # Verificar el token
        payload = verify_token(token, token_type="access")
        
        # Obtener user_id del payload
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Token sin user_id")
        
        # Buscar el usuario
        user = get_user_by_id(user_id)
        if not user:
            raise UnauthorizedException("Usuario no encontrado")
        
        # Verificar que el usuario esté activo
        if not user.get("is_active", True):
            raise UnauthorizedException("Usuario inactivo")
        
        # Agregar información del token al usuario
        user["token_role"] = payload.get("role")
        user["token_email"] = payload.get("email")
        
        logger.info(f"Usuario autenticado: {user['email']} (role: {user['role']})")
        return user
        
    except HTTPException:
        # Re-raise HTTP exceptions (ya tienen el formato correcto)
        raise
    except Exception as e:
        logger.error(f"Error al validar token: {str(e)}")
        raise UnauthorizedException(f"Error al validar token: {str(e)}")

# ============================================================================
# DEPENDENCY PARA VERIFICAR ROLES
# ============================================================================

class RoleChecker:
    """
    Dependency para verificar que el usuario tenga uno de los roles requeridos.
    
    Usage:
        @app.get("/admin/users")
        async def get_users(user: dict = Depends(RoleChecker(["admin"]))):
            ...
    """
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
    
    async def __call__(self, user: dict = Depends(get_current_user)) -> dict:
        """
        Verifica que el usuario tenga un rol permitido.
        
        Args:
            user: Usuario actual (obtenido de get_current_user)
            
        Returns:
            dict: Usuario si tiene permisos
            
        Raises:
            ForbiddenException: Si el usuario no tiene el rol requerido
        """
        user_role = user.get("role")
        
        if user_role not in self.allowed_roles:
            logger.warning(
                f"Acceso denegado: usuario {user.get('email')} "
                f"(role: {user_role}) intentó acceder a endpoint que requiere {self.allowed_roles}"
            )
            raise ForbiddenException(
                f"Requiere uno de estos roles: {', '.join(self.allowed_roles)}. "
                f"Tu rol actual: {user_role}"
            )
        
        logger.info(f"Acceso autorizado para {user.get('email')} con rol {user_role}")
        return user

# ============================================================================
# DECORADORES DE CONVENIENCIA
# ============================================================================

def require_admin(user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency que requiere rol de admin.
    
    Usage:
        @app.delete("/products/{product_id}")
        async def delete_product(
            product_id: int,
            user: dict = Depends(require_admin)
        ):
            ...
    """
    if user.get("role") != "admin":
        raise ForbiddenException("Solo administradores pueden realizar esta acción")
    return user

def require_admin_or_vendedor(user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency que requiere rol de admin o vendedor.
    
    Usage:
        @app.post("/products")
        async def create_product(
            product: ProductCreate,
            user: dict = Depends(require_admin_or_vendedor)
        ):
            ...
    """
    allowed_roles = ["admin", "vendedor"]
    if user.get("role") not in allowed_roles:
        raise ForbiddenException(
            f"Solo {' o '.join(allowed_roles)} pueden realizar esta acción"
        )
    return user

# ============================================================================
# MIDDLEWARE PARA LOGGING
# ============================================================================

class JWTLoggingMiddleware:
    """
    Middleware que registra todas las requests con información de autenticación.
    """
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Extraer información del request
            path = scope.get("path", "")
            method = scope.get("method", "")
            
            # Buscar el header Authorization
            headers = dict(scope.get("headers", []))
            auth_header = headers.get(b"authorization", b"").decode()
            
            has_token = "Bearer" in auth_header
            logger.info(f"{method} {path} - Token presente: {has_token}")
        
        # Continuar con el siguiente middleware/handler
        await self.app(scope, receive, send)

# ============================================================================
# UTILIDADES
# ============================================================================

def is_public_endpoint(path: str) -> bool:
    """
    Verifica si un endpoint es público (no requiere autenticación).
    
    Args:
        path: Ruta del endpoint
        
    Returns:
        bool: True si es público
    """
    public_paths = [
        "/",
        "/health",
        "/api/auth/login",
        "/api/auth/refresh",
        "/api/auth/test-users",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico",
    ]
    
    # Verificar paths exactos
    if path in public_paths:
        return True
    
    # Verificar paths con prefijos
    public_prefixes = ["/static/", "/assets/"]
    for prefix in public_prefixes:
        if path.startswith(prefix):
            return True
    
    return False

def extract_token_from_header(authorization: Optional[str]) -> Optional[str]:
    """
    Extrae el token JWT del header Authorization.
    
    Args:
        authorization: Valor del header Authorization
        
    Returns:
        str: Token JWT o None si no es válido
    """
    if not authorization:
        return None
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    
    return parts[1]

# ============================================================================
# EXPORTACIONES
# ============================================================================

__all__ = [
    "get_current_token",
    "get_current_user",
    "RoleChecker",
    "require_admin",
    "require_admin_or_vendedor",
    "UnauthorizedException",
    "ForbiddenException",
    "JWTLoggingMiddleware",
    "is_public_endpoint",
    "extract_token_from_header",
]
