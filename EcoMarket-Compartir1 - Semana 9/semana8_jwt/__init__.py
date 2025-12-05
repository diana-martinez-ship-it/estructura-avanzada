"""
Paquete JWT para EcoMarket - Semana 8
======================================

Sistema completo de autenticación JWT con:
- Generación y validación de tokens
- Middleware de seguridad
- Sistema de roles (admin, vendedor, cliente)
- Refresh tokens
"""

from . import auth
from . import models
from . import middleware

__version__ = "1.0.0"
__author__ = "EcoMarket Team"

__all__ = ["auth", "models", "middleware"]
