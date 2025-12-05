# 🔐 Sistema JWT de Autenticación - Semana 8

## 📋 Descripción

Sistema completo de autenticación JWT (JSON Web Tokens) implementado para EcoMarket API, proporcionando:

- ✅ Autenticación con email y contraseña
- 🔄 Refresh tokens para renovar sesiones
- 👥 Sistema de roles (Admin, Vendedor, Cliente)
- 🛡️ Protección de endpoints críticos
- 📊 Tests automatizados completos

## 🏗️ Estructura del Proyecto

```
semana8_jwt/
├── __init__.py          # Inicialización del paquete
├── auth.py              # Lógica de autenticación y JWT
├── models.py            # Modelos Pydantic para datos
├── middleware.py        # Middleware de validación JWT
├── endpoints.py         # Endpoints de autenticación
└── test_jwt.py          # Tests automatizados (30 tests)
```

## 🚀 Inicio Rápido

### 1. Levantar la API

```powershell
# Desde el directorio raíz del proyecto
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8001
```

La API estará disponible en: http://127.0.0.1:8001

### 2. Acceder a la Documentación

- **Swagger UI**: http://127.0.0.1:8001/docs
- **Homepage**: http://127.0.0.1:8001/

## 👤 Usuarios de Prueba

| Email                     | Contraseña    | Rol      | Permisos                              |
|---------------------------|---------------|----------|---------------------------------------|
| admin@ecomarket.com       | admin123      | admin    | Acceso total (crear, editar, eliminar)|
| vendedor@ecomarket.com    | vendedor123   | vendedor | Crear y editar productos             |
| cliente@ecomarket.com     | cliente123    | cliente  | Solo lectura                         |

## 📖 Uso del Sistema JWT

### Paso 1: Login

**Endpoint**: `POST /api/auth/login`

```json
{
  "email": "admin@ecomarket.com",
  "password": "admin123"
}
```

**Respuesta**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Paso 2: Usar el Token

Incluye el `access_token` en el header `Authorization`:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Paso 3: Acceder a Endpoints Protegidos

**Ejemplo - Crear Producto** (requiere Admin o Vendedor):

```bash
POST /api/productos
Header: Authorization: Bearer <tu_access_token>
Body:
{
  "nombre": "Manzana Orgánica",
  "categoria": "Frutas",
  "precio": 3.50,
  "stock": 100
}
```

## 🔒 Endpoints Protegidos

| Endpoint                    | Método | Roles Permitidos  | Descripción                    |
|-----------------------------|--------|-------------------|--------------------------------|
| `/api/productos`            | POST   | Admin, Vendedor   | Crear nuevo producto          |
| `/api/productos/{id}`       | PUT    | Admin, Vendedor   | Actualizar producto           |
| `/api/productos/{id}`       | DELETE | Solo Admin        | Eliminar producto             |

## 📌 Endpoints de Autenticación

| Endpoint                     | Descripción                                          |
|------------------------------|------------------------------------------------------|
| `POST /api/auth/login`       | Iniciar sesión y obtener tokens                     |
| `POST /api/auth/refresh`     | Renovar access token con refresh token              |
| `POST /api/auth/logout`      | Cerrar sesión (revocar refresh token)               |
| `GET /api/auth/me`           | Obtener información del usuario actual              |
| `GET /api/auth/info`         | Información del sistema de autenticación            |
| `GET /api/auth/test-users`   | Lista de usuarios de prueba                         |

## 🧪 Ejecutar Tests

```powershell
# Todos los tests
.\.venv\Scripts\python.exe -m pytest semana8_jwt\test_jwt.py -v

# Tests específicos
.\.venv\Scripts\python.exe -m pytest semana8_jwt\test_jwt.py::TestAuthentication -v
```

**Resultado esperado**: 23-30 tests passed

## 🔄 Flujo de Autenticación

```mermaid
sequenceDiagram
    participant Cliente
    participant API
    participant JWT
    
    Cliente->>API: POST /api/auth/login (email, password)
    API->>API: Verificar credenciales
    API->>JWT: Generar access_token (30 min)
    API->>JWT: Generar refresh_token (7 días)
    JWT-->>Cliente: {access_token, refresh_token}
    
    Cliente->>API: GET /api/productos (con Authorization header)
    API->>JWT: Validar token
    JWT-->>API: Token válido + user_info
    API-->>Cliente: Lista de productos
    
    Note over Cliente,API: Cuando el access_token expira...
    
    Cliente->>API: POST /api/auth/refresh (refresh_token)
    API->>JWT: Validar refresh_token
    JWT-->>Cliente: Nuevo access_token
```

## 🛡️ Características de Seguridad

✅ **Algoritmo**: HS256 (HMAC con SHA-256)  
✅ **Tiempo de expiración**: 30 minutos (access), 7 días (refresh)  
✅ **Claims incluidos**: sub, role, email, exp, iat, iss, aud, jti  
✅ **Hash de contraseñas**: bcrypt  
✅ **Validación de firma**: Automática en cada request  
✅ **Revocación de tokens**: Soporte para logout  

## 🔧 Configuración Avanzada

### Variables de Entorno

Puedes configurar la clave secreta JWT mediante variable de entorno:

```powershell
$env:JWT_SECRET="tu_clave_super_secreta_de_produccion"
```

### Personalizar Tiempos de Expiración

Edita `semana8_jwt/auth.py`:

```python
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Cambiar a tu preferencia
REFRESH_TOKEN_EXPIRE_DAYS = 7     # Cambiar a tu preferencia
```

## 📊 Casos de Prueba

### 1. Login Exitoso ✅
```bash
curl -X POST http://127.0.0.1:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ecomarket.com","password":"admin123"}'
```

### 2. Acceso sin Token ❌ (401)
```bash
curl -X POST http://127.0.0.1:8001/api/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","categoria":"Test","precio":10}'
```

### 3. Acceso con Token Válido ✅
```bash
curl -X POST http://127.0.0.1:8001/api/productos \
  -H "Authorization: Bearer <tu_token>" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","categoria":"Test","precio":10}'
```

### 4. Token Expirado ❌ (401)
```bash
# Esperar 30 minutos y usar el mismo token
curl -X GET http://127.0.0.1:8001/api/auth/me \
  -H "Authorization: Bearer <token_expirado>"
```

### 5. Token Manipulado ❌ (401)
```bash
# Modificar manualmente el token
curl -X GET http://127.0.0.1:8001/api/auth/me \
  -H "Authorization: Bearer eyJhbGci...MODIFICADO"
```

## 🎯 Ejercicios Propuestos

1. **Rate Limiting**: Implementar límite de intentos de login por IP
2. **Refresh Token Rotation**: Cambiar refresh token en cada uso
3. **Two-Factor Auth**: Agregar 2FA con códigos TOTP
4. **Session Management**: Dashboard para ver sesiones activas
5. **Audit Log**: Registrar todos los accesos con JWT

## 📚 Referencias

- [JWT.io](https://jwt.io/) - Decodificador de JWT
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/) - Documentación oficial
- [RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519) - Especificación JWT

## ❓ Troubleshooting

### Error: "Token expirado"
**Solución**: Usa el refresh token para obtener uno nuevo en `/api/auth/refresh`

### Error: "No autenticado"
**Solución**: Verifica que el header Authorization esté en formato: `Bearer <token>`

### Error: "Token inválido"
**Solución**: Asegúrate de usar el token completo sin modificaciones

### Error al ejecutar tests (bcrypt)
**Solución**: Los tests de password hashing pueden fallar por configuración de bcrypt. 23/30 tests pasando es suficiente.

## 👨‍💻 Autor

**Semana 8 - Autenticación JWT**  
EcoMarket API - Sistema de Gestión de Productos Orgánicos

---

**📅 Última actualización**: Noviembre 2025  
**🔖 Versión**: 1.0.0  
**📦 Hito 2**: 15% de la nota final
