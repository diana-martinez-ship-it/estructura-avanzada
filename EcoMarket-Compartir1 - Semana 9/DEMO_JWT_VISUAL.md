# 🔒 Demo Interactiva JWT + HTTPS - Guía de Presentación

## 📋 Descripción General

Esta es una demostración visual completa del **Hito 2: Autenticación JWT + HTTPS/TLS + Gestión de Secretos**, diseñada específicamente para presentación al maestro sin necesidad de usar Swagger.

---

## 🎯 Objetivo

Demostrar de manera visual e interactiva:
1. **JWT Authentication (Semana 8)**: Login, generación de tokens, uso en endpoints protegidos
2. **HTTPS/TLS (Semana 9)**: Cifrado de comunicaciones
3. **Gestión de Secretos (Semana 9)**: Uso de pydantic-settings y .env

---

## 🚀 Cómo Acceder a la Demo

### Opción 1: Desde la Página Principal
1. Abre: `https://localhost:8443`
2. Busca la sección **"🔒 Sistema de Seguridad Implementado"**
3. Haz clic en el botón naranja: **"🔒 Demo Interactiva JWT + HTTPS"**

### Opción 2: Directamente
1. Abre directamente: `https://localhost:8443/jwt-demo`

---

## 📝 Guía Paso a Paso para la Presentación

### **Paso 1: Explicar el Indicador de Seguridad** 🔒

Al abrir la página, verás en la parte superior:
```
🔒 Conexión Segura Activa
HTTPS en puerto 8443
```

**Explicación para el maestro:**
- ✅ Esto confirma que la conexión está cifrada con TLS
- ✅ Puerto 8443 es el puerto estándar alternativo para HTTPS
- ✅ Todos los datos viajan encriptados (no pueden ser interceptados)

---

### **Paso 2: Obtener Token JWT (Login)** 🎫

**Instrucciones:**
1. En la sección **"Paso 1: Obtener Token JWT (Login)"**
2. Selecciona uno de los 3 usuarios disponibles:
   - 🔑 **Admin** (Acceso completo)
   - 🛍️ **Vendedor** (Crear y editar productos)
   - 👤 **Cliente** (Solo lectura)
3. Haz clic en **"🚀 Hacer Login"**

**Resultado:**
- ✅ Aparece un token JWT largo (ejemplo: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)
- ✅ Se muestra la información del usuario
- ✅ El botón del Paso 2 se activa

**Explicación para el maestro:**
- El servidor validó las credenciales
- Generó un JWT firmado con `JWT_SECRET` del archivo .env
- El token viaja cifrado por HTTPS
- El token expira en 30 minutos (configurado en `config.py`)
- Contiene información del usuario (email, rol, permisos)

---

### **Paso 3: Usar Token en Endpoint Protegido** 🔐

**Instrucciones:**
1. Una vez que tienes el token, el botón **"✅ Crear Producto (Token Cargado)"** se habilita
2. Puedes modificar los datos del producto si quieres:
   - Nombre del producto
   - Categoría
   - Precio
   - Stock
   - Descripción
3. Haz clic en **"✅ Crear Producto (Token Cargado)"**

**Resultado:**
- ✅ Aparece respuesta `200 OK` con el producto creado
- ✅ Se muestra el JSON completo del producto creado (con ID, timestamps, etc.)

**Explicación para el maestro:**
- El endpoint `/api/productos` está protegido por JWT middleware
- El token se envía en el header: `Authorization: Bearer <token>`
- El servidor verifica la firma del token con `JWT_SECRET`
- Si el token es válido y el rol tiene permisos → 200 OK
- El producto se crea correctamente en la base de datos

---

### **Paso 4: Probar SIN Token (Debe Fallar)** ❌

**Instrucciones:**
1. En la sección **"Paso 3: Probar SIN Token (Debe Fallar)"**
2. Haz clic en **"⚠️ Intentar Crear Producto SIN Token"**

**Resultado:**
- ❌ Aparece error `401 Unauthorized`
- ❌ Mensaje: `"Not authenticated"` o similar
- ✅ Confirmación: **"¡La seguridad funciona!"**

**Explicación para el maestro:**
- Esto demuestra que la autenticación JWT funciona correctamente
- Sin token válido → Acceso denegado
- Endpoints protegidos NO son accesibles sin autenticación
- La seguridad está implementada correctamente

---

## 🎓 Puntos Clave para Destacar al Maestro

### 1. **JWT Authentication (Semana 8)** ✅
- ✅ Algoritmo: HS256 (HMAC con SHA-256)
- ✅ Secretos diferentes para access y refresh tokens
- ✅ Roles implementados: admin, vendedor, cliente
- ✅ Tokens de refresco con duración de 7 días
- ✅ Sistema de logout con revocación de tokens
- ✅ 30 tests automatizados (Semana 8)

### 2. **HTTPS/TLS (Semana 9)** ✅
- ✅ TLS 1.2/1.3 activo
- ✅ Puerto 8443 (estándar alternativo HTTPS)
- ✅ Certificados RSA 4096 bits
- ✅ Middleware de redirección HTTP→HTTPS (producción)
- ✅ Toda la comunicación cifrada

### 3. **Gestión de Secretos (Semana 9)** ✅
- ✅ `pydantic-settings` para configuración
- ✅ Archivo `.env` con secretos externalizados
- ✅ Validaciones automáticas (longitud mínima, unicidad)
- ✅ `.gitignore` configurado (secretos no en repositorio)
- ✅ Sin hardcode de credenciales

---

## 📊 Resumen Visual de la Demo

La página incluye un **resumen visual** al final con 3 columnas:

### 🎫 JWT (Semana 8)
- Algoritmo HS256
- Roles: admin, vendedor, cliente
- Refresh tokens (7 días)
- 30 tests automatizados

### 🔒 HTTPS (Semana 9)
- TLS 1.2/1.3
- Puerto 8443
- Certificados RSA 4096
- Redirección HTTP→HTTPS

### 🔑 Secretos (Semana 9)
- pydantic-settings
- .env gitignored
- Validación automática
- Sin hardcode

---

## 💡 Ventajas de Esta Demo Visual

### ✅ **Facilidad de Uso**
- No requiere conocimientos de Swagger
- Interfaz intuitiva y guiada
- Explicaciones en cada paso

### ✅ **Completitud**
- Demuestra todos los requisitos de Semana 8 y 9
- Flujo completo: login → token → uso → fallo sin token

### ✅ **Profesionalidad**
- Diseño moderno y atractivo
- Colores consistentes (púrpura/naranja)
- Indicadores visuales claros (✅ ❌ ⚠️)

### ✅ **Educativa**
- Explicaciones claras en cada sección
- Cuadros informativos ("💡 ¿Qué está pasando aquí?")
- Demuestra tanto éxitos como fallos de seguridad

---

## 🔄 Flujo Completo de la Demo

```
1. Abrir https://localhost:8443/jwt-demo
   ↓
2. Verificar indicador HTTPS (🔒 verde)
   ↓
3. Paso 1: Login con usuario (admin/vendedor/cliente)
   ↓
4. Ver token JWT generado
   ↓
5. Paso 2: Crear producto CON token → ✅ 200 OK
   ↓
6. Paso 3: Crear producto SIN token → ❌ 401 Unauthorized
   ↓
7. Revisar resumen de implementaciones (final de página)
```

---

## 📱 Consejos para la Presentación

### **Durante la Demo:**
1. **Muestra el indicador HTTPS primero** - Destaca que es verde y dice "Conexión Segura"
2. **Explica cada paso ANTES de hacerlo** - No hagas clic sin explicar qué va a pasar
3. **Lee los cuadros informativos** - Tienen explicaciones técnicas importantes
4. **Muestra el token completo** - Puedes hacer scroll en el cuadro negro para mostrarlo
5. **Destaca el error 401** - Demuestra que la seguridad funciona

### **Puntos a Mencionar:**
- "El token viaja cifrado por HTTPS, nadie puede interceptarlo"
- "El secreto JWT_SECRET está en el archivo .env, no en el código"
- "pydantic-settings valida automáticamente que los secretos cumplan requisitos"
- "30 tests automatizados validan que todo funcione correctamente"

### **Si el Maestro Pregunta:**
- **"¿Dónde están los secretos?"** → Muestra el archivo `.env` (pero NO muestres los valores reales)
- **"¿Cómo se generan los certificados?"** → Explica el script `generar_certificados.py`
- **"¿Qué pasa en producción?"** → Explica que se usarían certificados de Let's Encrypt
- **"¿Por qué puerto 8443?"** → Es el puerto estándar alternativo para HTTPS (443 requiere admin)

---

## 🎯 Checklist de Presentación

Antes de presentar, verifica:
- [ ] Servidor corriendo en `https://localhost:8443`
- [ ] Página `/jwt-demo` accesible
- [ ] Indicador HTTPS muestra "🔒 Conexión Segura Activa"
- [ ] Login funciona con los 3 usuarios
- [ ] Crear producto CON token funciona (200 OK)
- [ ] Crear producto SIN token falla (401 Unauthorized)
- [ ] Todos los cuadros informativos se muestran correctamente

---

## 📚 Documentación Relacionada

- `HTTPS_SETUP.md` - Guía técnica completa de HTTPS
- `DEMO_PRESENTACION.md` - Guía general de presentación
- `SEMANA9_COMPLETADA.md` - Resumen de implementación Semana 9
- `README.md` - Documentación principal del proyecto

---

## 🎉 Conclusión

Esta demo visual permite presentar de manera clara y profesional:
- ✅ Todo el **Hito 2** (JWT + HTTPS + Secretos)
- ✅ Funcionalidad completa en **interfaz web**
- ✅ Sin necesidad de usar Swagger o herramientas externas
- ✅ Explicaciones educativas en cada paso

**¡Todo implementado visualmente en la API, tal como solicitaste!** 🚀
