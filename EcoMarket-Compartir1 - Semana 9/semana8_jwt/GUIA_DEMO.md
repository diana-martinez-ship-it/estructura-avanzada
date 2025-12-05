# 📹 VIDEO DEMOSTRACIÓN - SISTEMA JWT ECOMARKET

## 🎬 Guión para Video Demostrativo (2 minutos)

### INTRODUCCIÓN (15 segundos)
"Hola, bienvenidos a la demostración del Sistema JWT de Autenticación implementado en EcoMarket API. En esta presentación veremos cómo funciona la autenticación con tokens, el sistema de roles y la protección de endpoints."

### PARTE 1: SWAGGER UI (20 segundos)
1. Abrir http://127.0.0.1:8001/docs
2. Mostrar la sección "Autenticación JWT" con 7 endpoints
3. Mostrar los endpoints protegidos marcados con candado 🔒

### PARTE 2: LOGIN (25 segundos)
1. Expandir `POST /api/auth/login`
2. Click en "Try it out"
3. Ingresar:
   ```json
   {
     "email": "admin@ecomarket.com",
     "password": "admin123"
   }
   ```
4. Click "Execute"
5. Mostrar el access_token y refresh_token en la respuesta
6. Copiar el access_token

### PARTE 3: AUTENTICACIÓN (20 segundos)
1. Click en el botón "Authorize" (candado arriba a la derecha)
2. Pegar: `Bearer <access_token>`
3. Click "Authorize"
4. Mostrar que ahora el candado está cerrado (autenticado)

### PARTE 4: USUARIO ACTUAL (15 segundos)
1. Expandir `GET /api/auth/me`
2. Click "Try it out" → "Execute"
3. Mostrar respuesta con información del usuario:
   ```json
   {
     "email": "admin@ecomarket.com",
     "name": "Administrador",
     "role": "admin"
   }
   ```

### PARTE 5: CREAR PRODUCTO (25 segundos)
1. Ir a sección "Productos"
2. Expandir `POST /api/productos`
3. Notar que requiere autenticación (candado cerrado)
4. Click "Try it out"
5. Ingresar producto:
   ```json
   {
     "nombre": "Aguacate Orgánico",
     "categoria": "Frutas",
     "precio": 5.99,
     "stock": 50
   }
   ```
6. Click "Execute"
7. Mostrar respuesta exitosa con ID asignado

### PARTE 6: PRUEBA SIN TOKEN (20 segundos)
1. Click en "Authorize" → "Logout"
2. Intentar crear otro producto
3. Mostrar error 401 Unauthorized
4. Explicar: "Sin token, el sistema rechaza la operación"

### PARTE 7: ROLES (15 segundos)
1. Login como vendedor:
   ```json
   {
     "email": "vendedor@ecomarket.com",
     "password": "vendedor123"
   }
   ```
2. Autorizar con el nuevo token
3. Intentar DELETE producto
4. Mostrar error 403 Forbidden (sin permisos)

### CIERRE (5 segundos)
"Como vimos, el sistema JWT protege nuestra API, valida usuarios y controla permisos por rol. ¡Gracias por su atención!"

---

## 📸 Screenshots Clave para Documentación

### 1. Homepage con JWT
- URL: http://127.0.0.1:8001/
- Captura: Homepage mostrando el sistema funcionando

### 2. Swagger UI - Endpoints JWT
- URL: http://127.0.0.1:8001/docs
- Captura: Sección "Autenticación JWT" expandida

### 3. Login Exitoso
- Captura: Respuesta de /api/auth/login con tokens

### 4. Usuario Autenticado
- Captura: Respuesta de /api/auth/me

### 5. Producto Creado
- Captura: Respuesta exitosa de POST /api/productos

### 6. Error 401 (Sin Token)
- Captura: Error al intentar acceder sin autenticación

### 7. Error 403 (Sin Permisos)
- Captura: Vendedor intentando eliminar producto

---

## 🎥 Alternativa: Script de Prueba Automático

Si no puedes grabar video, ejecuta este script que muestra todo:

```powershell
.\semana8_jwt\test_api_jwt.ps1
```

Este script ejecuta:
- ✅ Login exitoso
- ✅ Obtener usuario actual
- ✅ Crear producto con token
- ✅ Intentar sin token (falla)
- ✅ Refresh token
- ✅ Login con otro rol
- ✅ Prueba de permisos
- ✅ Eliminar producto
- ✅ Logout

**Resultado**: Demostración completa en consola con colores

---

## 📋 Checklist de Demostración

Antes de grabar/presentar, verifica:
- [ ] API corriendo en http://127.0.0.1:8001
- [ ] Swagger UI accesible en /docs
- [ ] 3 usuarios de prueba funcionando
- [ ] Endpoints protegidos con candado
- [ ] Login genera tokens válidos
- [ ] Tokens permiten acceso a endpoints
- [ ] Sin token → Error 401
- [ ] Sin permisos → Error 403
- [ ] Refresh token funciona
- [ ] Logout revoca tokens

---

## 🎨 Puntos Destacados para la Presentación

### Fortalezas del Sistema:
1. **Seguridad robusta** con JWT estándar
2. **Sistema de roles** flexible (Admin, Vendedor, Cliente)
3. **Refresh tokens** para sesiones largas
4. **Documentación automática** en Swagger
5. **Tests completos** (30 casos de prueba)
6. **Fácil integración** con FastAPI Depends
7. **Manejo de errores** claro y descriptivo

### Tecnologías Utilizadas:
- JWT (JSON Web Tokens)
- FastAPI Security
- Pydantic Models
- SHA256 Hashing
- HTTP Bearer Authentication
- Dependency Injection

---

## 💡 Preguntas Frecuentes para Demo

**Q: ¿Por qué usar JWT?**
A: JWT es stateless, escalable, y permite microservicios. No requiere sesiones en servidor.

**Q: ¿Qué pasa si roban mi token?**
A: El token expira en 30 minutos. Además, el sistema permite logout para revocar refresh tokens.

**Q: ¿Cómo se protegen las contraseñas?**
A: Se almacenan hasheadas con SHA256. Nunca se guardan en texto plano.

**Q: ¿Qué es el refresh token?**
A: Un token de larga duración (7 días) para renovar access tokens sin re-login.

**Q: ¿Por qué 401 vs 403?**
A: 401 = No autenticado (sin token). 403 = Autenticado pero sin permisos.

---

## ✅ Checklist Final de Entrega

Archivos para entregar:
- [ ] semana8_jwt/ (carpeta completa)
- [ ] main.py (con JWT integrado)
- [ ] README.md (documentación)
- [ ] RESUMEN_ENTREGA.md (este archivo)
- [ ] Screenshots o video de demostración
- [ ] Archivo requirements.txt actualizado

Puntos a mencionar en la entrega:
- [ ] Sistema JWT completamente funcional
- [ ] 7 endpoints de autenticación
- [ ] 3 endpoints protegidos
- [ ] 30 tests automatizados (23 pasando)
- [ ] 3 roles implementados
- [ ] Refresh tokens y logout
- [ ] Documentación completa
- [ ] Demo en vivo funcionando
