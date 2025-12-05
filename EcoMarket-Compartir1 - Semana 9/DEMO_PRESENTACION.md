# 🎓 Guía de Presentación - Hito 2: Seguridad en EcoMarket

## 📋 Preparación Antes de la Demo (5 minutos antes)

```powershell
# 1. Navegar al proyecto
cd C:\Users\jospa\OneDrive\Documentos\Universidad\EligardoTareas\EcoMarket-Compartir\EcoMarket-Compartir1

# 2. Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# 3. Iniciar servidor con HTTPS
python main.py
```

**Verifica que veas:**
```
🔒 Iniciando EcoMarket API con HTTPS (TLS/SSL)
📍 URL: https://localhost:8443
```

---

## 🎬 Script de Presentación (10-15 minutos)

### 1️⃣ INTRODUCCIÓN (1 min)

> "Buenos días/tardes profesor. Voy a demostrar la implementación completa del **Hito 2: Seguridad en Sistemas Distribuidos**, que incluye:
> - ✅ **Autenticación JWT** (Semana 8)
> - ✅ **Cifrado HTTPS/TLS** (Semana 9)
> - ✅ **Gestión de Secretos** (Semana 9)"

---

### 2️⃣ DEMOSTRACIÓN DE SECRETOS (3 min)

**Abrir ventana de código:**

1. **Mostrar `.env.example`:**
```powershell
cat .env.example
```

> "Este es el archivo de plantilla que se versiona en Git. Los valores reales NO están aquí."

2. **Mostrar que `.env` NO está en Git:**
```powershell
git status
# .env NO debe aparecer

cat .gitignore | Select-String -Pattern "\.env"
# Debe mostrar .env en la lista
```

3. **Mostrar `config.py`:**
```powershell
cat config.py
```

> "La configuración usa **pydantic-settings** con validaciones automáticas:
> - JWT_SECRET mínimo 32 caracteres
> - JWT_SECRET ≠ JWT_REFRESH_SECRET
> - Si falta algún secreto, la app NO inicia"

**Demostración práctica:**
```powershell
# Simular secreto faltante
$env:JWT_SECRET = ""
python -c "from config import settings"
# Debe fallar con error claro
```

---

### 3️⃣ DEMOSTRACIÓN DE CERTIFICADOS SSL (3 min)

1. **Mostrar script de generación:**
```powershell
cat generar_certificados.py | Select-Object -First 30
```

> "Este script genera certificados autofirmados con:
> - RSA 4096 bits
> - Válidos por 365 días
> - Subject Alternative Names para localhost"

2. **Verificar certificados existen:**
```powershell
ls certs
# Debe mostrar cert.pem y key.pem
```

3. **Mostrar que certificados NO están en Git:**
```powershell
cat .gitignore | Select-String -Pattern "\.pem|certs"
```

---

### 4️⃣ DEMOSTRACIÓN DE HTTPS EN ACCIÓN (5 min)

**A. Mostrar Servidor Corriendo**

```powershell
# El servidor ya debe estar corriendo
# Mostrar la terminal con el mensaje de HTTPS
```

**B. Abrir Navegador - Verificar Candado 🔒**

1. Navegar a: `https://localhost:8443`
2. Hacer clic en el candado 🔒 en la barra de direcciones
3. Mostrar: "Certificado" → Emisor: "EcoMarket Dev" → Válido hasta

> "El navegador muestra advertencia porque es autofirmado, pero en producción usaríamos Let's Encrypt."

**C. Documentación Interactiva**

4. Ir a: `https://localhost:8443/docs`
5. Mostrar la interfaz Swagger

> "Toda la API está documentada automáticamente con OpenAPI/Swagger."

**D. Probar Autenticación JWT sobre HTTPS**

6. En `/docs`, expandir **POST /api/auth/login**
7. Click en "Try it out"
8. Usar credenciales:
```json
{
  "email": "admin@ecomarket.com",
  "password": "admin123"
}
```
9. Click "Execute"
10. Mostrar respuesta con `access_token` y `refresh_token`

> "El token JWT viaja cifrado por HTTPS. Sin HTTPS, podría ser interceptado en una red WiFi pública."

**E. Usar el Token en Endpoint Protegido**

11. Copiar el `access_token` de la respuesta
12. Expandir **POST /api/productos**
13. Click en "Try it out"
14. Click en el candado 🔒 verde ("Authorize")
15. Pegar: `Bearer <tu_token>`
16. Click "Authorize" y cerrar
17. Llenar datos del producto:
```json
{
  "nombre": "Producto Demo Maestro",
  "categoria": "Demostración",
  "precio": 99.99,
  "disponible": true,
  "stock": 100,
  "descripcion": "Creado durante la demostración del Hito 2"
}
```
18. Click "Execute"
19. Mostrar respuesta exitosa (201 Created)

> "Este endpoint requiere autenticación. Sin el token JWT, devolvería 401 Unauthorized."

**F. Probar sin Token (403 Forbidden)**

20. Click en el candado verde → "Logout"
21. Expandir **DELETE /api/productos/{id}**
22. Intentar borrar producto con ID 1
23. Mostrar error 401

> "La seguridad funciona: sin autenticación, no hay acceso."

---

### 5️⃣ DEMOSTRACIÓN CON CURL (2 min)

**Abrir PowerShell nueva:**

```powershell
# A. Health check simple
curl -k https://localhost:8443/health

# B. Login y capturar token
$response = Invoke-RestMethod -Uri "https://localhost:8443/api/auth/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"email":"admin@ecomarket.com","password":"admin123"}' `
  -SkipCertificateCheck

$token = $response.access_token
Write-Host "Token obtenido: $($token.Substring(0,20))..."

# C. Usar token en endpoint protegido
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Uri "https://localhost:8443/api/productos" `
  -Method GET `
  -Headers $headers `
  -SkipCertificateCheck
```

---

### 6️⃣ MOSTRAR CÓDIGO CLAVE (2 min)

**A. Configuración HTTPS en `main.py`:**

```powershell
cat main.py | Select-String -Pattern "ssl_" -Context 2,2
```

**B. Middleware de Redirección (solo producción):**

```powershell
cat main.py | Select-String -Pattern "HTTPSRedirect" -Context 3,3
```

> "El middleware de redirección HTTP→HTTPS solo se activa en producción para evitar loops en desarrollo."

---

### 7️⃣ DOCUMENTACIÓN (1 min)

**Mostrar archivos de documentación:**

```powershell
ls *.md
# README.md, HTTPS_SETUP.md, etc.

# Mostrar tabla de contenidos
cat HTTPS_SETUP.md | Select-Object -First 20
```

> "Toda la configuración está documentada paso a paso:
> - Generación de certificados
> - Configuración de secretos
> - Troubleshooting
> - Guía para producción con Let's Encrypt y Nginx"

---

### 8️⃣ ARQUITECTURA Y CAPAS DE SEGURIDAD (1 min)

**Abrir diagrama (puedes dibujar en pizarra o mostrar):**

```
┌─────────────────────────────────────────┐
│  👤 Cliente (Navegador/Postman)         │
└──────────────┬──────────────────────────┘
               │ HTTPS (TLS 1.2/1.3) 🔒
               │ ⚡ Cifrado E2E
               ▼
┌─────────────────────────────────────────┐
│  🔐 Nginx/ALB (SSL Termination)         │
│  • Certificado Let's Encrypt            │
│  • Renovación automática                │
└──────────────┬──────────────────────────┘
               │ HTTP Interno
               │ (Red privada)
               ▼
┌─────────────────────────────────────────┐
│  🎫 FastAPI + JWT Middleware            │
│  • Valida token en cada request         │
│  • Verifica roles (admin/vendedor)      │
│  • Firma con SECRET del .env            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  💾 Base de Datos                       │
│  • Conexión TLS                         │
│  • Passwords hasheados (SHA256)         │
└─────────────────────────────────────────┘

SECRETOS: .env / Vault / Cloud Secrets
```

> "Tres capas de seguridad:
> 1. **HTTPS** protege datos en tránsito
> 2. **JWT** autentica y autoriza usuarios
> 3. **Secretos externalizados** evitan leaks en Git"

---

## 🎯 CIERRE (1 min)

> "En resumen, he implementado:
> 
> ✅ **Semana 8 - JWT:** Autenticación con tokens, roles (admin/vendedor/cliente), refresh tokens, 30 tests automatizados
> 
> ✅ **Semana 9 - HTTPS:** Certificados SSL autofirmados para dev, servidor en puerto 8443, middleware de redirección
> 
> ✅ **Semana 9 - Secretos:** pydantic-settings con validaciones, .env gitignored, config.py centralizado
> 
> El sistema está listo para **desarrollo local seguro** y documentado para **producción con Let's Encrypt**."

---

## 📸 Capturas Sugeridas para Informe

Si el maestro requiere informe escrito, incluye:

1. **Terminal con servidor HTTPS corriendo** (puerto 8443)
2. **Navegador mostrando candado 🔒** en `https://localhost:8443`
3. **Swagger UI** (`/docs`) con endpoint de login
4. **Respuesta de login** con `access_token` y `refresh_token`
5. **Endpoint protegido con token** (201 Created)
6. **Endpoint protegido SIN token** (401 Unauthorized)
7. **Código de `config.py`** con validaciones
8. **Código de `main.py`** con configuración SSL
9. **`.gitignore`** mostrando `.env` y `*.pem`
10. **Estructura de archivos** (`ls` mostrando `certs/`, `config.py`, etc.)

---

## 🎬 Tips para una Demo Exitosa

### ✅ HACER:
- Tener todo configurado 5 minutos antes
- Servidor ya corriendo con HTTPS
- Navegador con pestañas preparadas (`/docs`, `/`)
- Terminal lista con comandos copiados
- Hablar con confianza: "Este sistema implementa..."
- Explicar el **POR QUÉ**: "Usamos HTTPS porque sin él, un atacante en WiFi público podría..."

### ❌ EVITAR:
- Empezar a instalar dependencias durante la demo
- Errores de typo en comandos (usa copiar-pegar)
- Decir "no sé" → Decir "eso está documentado en HTTPS_SETUP.md línea X"
- Demo más de 15 minutos (pierde atención)
- Leer código línea por línea (resalta lo importante)

---

## 🚨 Plan B: Si Algo Falla

### Error: Certificado no válido
```powershell
# Regenerar rápido
python generar_certificados.py
python main.py
```

### Error: Puerto ocupado
```powershell
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force
python main.py
```

### Error: .env no carga
```powershell
# Verificar
cat .env | Select-String -Pattern "JWT_SECRET"

# Si falta, copiar desde .env.example
cp .env.example .env
# Editar manualmente
```

---

## 📊 Checklist Final Antes de Presentar

- [ ] Servidor corriendo en `https://localhost:8443`
- [ ] Navegador abierto en `/docs`
- [ ] Token de admin listo para copiar
- [ ] Comandos curl preparados en terminal
- [ ] Código de `config.py` y `main.py` abiertos en VS Code
- [ ] Documentación `HTTPS_SETUP.md` visible
- [ ] `.gitignore` mostrando exclusiones
- [ ] Tests ejecutados: `pytest semana8_jwt/test_jwt.py -v`
- [ ] Sin errores en consola (solo warnings de pydantic OK)

---

## 🏆 Bonus: Preguntas Comunes del Maestro

**P: "¿Por qué no usar HTTP simple?"**
> "HTTP envía datos en texto plano. Un atacante en una red WiFi pública puede interceptar tokens JWT y contraseñas usando herramientas como Wireshark. HTTPS cifra todo el canal con TLS."

**P: "¿Qué pasa si alguien roba tu JWT_SECRET?"**
> "Puede generar tokens falsos para cualquier usuario. Por eso:
> 1. Está en .env (no en código)
> 2. .gitignore lo excluye de Git
> 3. En producción usaríamos Vault o AWS Secrets Manager
> 4. Lo rotamos cada 90 días"

**P: "¿Este certificado sirve para producción?"**
> "No, es autofirmado solo para desarrollo. En producción usaríamos Let's Encrypt (gratuito) o certificados comerciales. Está documentado en HTTPS_SETUP.md sección 'Producción'."

**P: "¿Cómo manejas múltiples entornos (dev, staging, prod)?"**
> "Cada entorno tiene su propio .env:
> - .env.development (localhost)
> - .env.staging (AWS staging)
> - .env.production (AWS prod)
> La variable ENVIRONMENT en config.py controla comportamientos como el middleware de redirección HTTPS."

**P: "¿Hiciste tests?"**
> "Sí, 30 tests automatizados en semana8_jwt/test_jwt.py que cubren:
> - Generación y validación de tokens
> - Expiración y manipulación
> - Roles y permisos
> - Flujo completo de autenticación"

---

## 📝 Entregables Sugeridos

1. **Código fuente** (repositorio Git o ZIP)
2. **Documento PDF** con capturas de pantalla
3. **Video de 3-5 minutos** mostrando:
   - Login con JWT
   - Token protegiendo endpoint
   - HTTPS en navegador con candado
4. **Informe técnico** explicando decisiones de diseño

---

## 🎓 Argumento de Calificación Máxima

> "Este proyecto implementa las **tres capas de seguridad críticas** en sistemas distribuidos:
> 
> 1. **Identidad** (JWT): Sé quién eres y qué puedes hacer
> 2. **Confidencialidad** (HTTPS): Los datos viajan cifrados
> 3. **Configuración** (Secretos): Las llaves están protegidas
> 
> Cumple con estándares de la industria (OWASP, Twelve-Factor App) y está listo para evolucionar a producción con Let's Encrypt y Nginx. La documentación permite que cualquier desarrollador configure el sistema en menos de 5 minutos."

---

¡Éxito en tu presentación! 🚀
