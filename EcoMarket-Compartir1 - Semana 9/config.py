"""
Configuración centralizada de EcoMarket API
Usando pydantic-settings para validación y tipado
"""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache

# Cargar variables de entorno del archivo .env
load_dotenv()

class Settings(BaseSettings):
    """
    Configuración de la aplicación con validación automática.
    Los valores se cargan desde variables de entorno o archivo .env
    """
    
    # Base de datos (opcional por ahora)
    database_url: str = ""
    
    # JWT - Autenticación
    jwt_secret: str
    jwt_refresh_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # Entorno
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        # Mapeo de nombres de variables de entorno a atributos
        fields = {
            "database_url": {"env": "DB_URL"},
            "jwt_secret": {"env": "JWT_SECRET"},
            "jwt_refresh_secret": {"env": "JWT_REFRESH_SECRET"},
            "jwt_algorithm": {"env": "JWT_ALGORITHM"},
            "jwt_expire_minutes": {"env": "JWT_EXPIRE_MINUTES"},
            "environment": {"env": "ENVIRONMENT"},
        }

@lru_cache()  # Singleton - carga una sola vez
def get_settings() -> Settings:
    """
    Obtiene la instancia única de configuración.
    Usa @lru_cache para garantizar que solo se carga una vez.
    """
    return Settings()

# Instancia global de configuración
settings = get_settings()

# ============================================================================
# Validaciones de Seguridad
# ============================================================================

# Verificar longitud mínima del JWT_SECRET
if len(settings.jwt_secret) < 32:
    raise ValueError(
        "❌ JWT_SECRET debe tener al menos 32 caracteres para ser seguro.\n"
        f"   Longitud actual: {len(settings.jwt_secret)} caracteres\n"
        "   Genera una clave segura con: openssl rand -hex 32"
    )

# Verificar que JWT_SECRET y JWT_REFRESH_SECRET sean diferentes
if settings.jwt_secret == settings.jwt_refresh_secret:
    raise ValueError(
        "❌ JWT_SECRET y JWT_REFRESH_SECRET deben ser diferentes.\n"
        "   Usa claves distintas para access tokens y refresh tokens.\n"
        "   Genera otra clave con: openssl rand -hex 32"
    )

# Logging de configuración (sin mostrar secretos)
print("✅ Configuración cargada exitosamente:")
print(f"   • Entorno: {settings.environment}")
print(f"   • Algoritmo JWT: {settings.jwt_algorithm}")
print(f"   • Expiración JWT: {settings.jwt_expire_minutes} minutos")
print(f"   • JWT_SECRET: {settings.jwt_secret[:8]}... (oculto por seguridad)")
if settings.database_url:
    print(f"   • Base de datos: Configurada")
else:
    print(f"   • Base de datos: No configurada (opcional)")
