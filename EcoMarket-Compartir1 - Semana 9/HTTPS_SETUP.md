# 🔒 Guía de Configuración HTTPS y Seguridad - EcoMarket API

## 📋 Tabla de Contenidos

1. [Gestión de Secretos (.env)](#gestión-de-secretos-env)
2. [Generación de Certificados SSL](#generación-de-certificados-ssl)
3. [Ejecución con HTTPS](#ejecución-con-https)
4. [Troubleshooting](#troubleshooting)
5. [Producción](#producción)

---

## 🔐 Gestión de Secretos (.env)

### ¿Por qué es importante?

**NUNCA** debes incluir secretos (contraseñas, claves JWT, API keys) directamente en el código. Los secretos deben estar en variables de entorno, fuera del repositorio Git.

### Configuración Inicial

1. **Copia el archivo de plantilla:**
   ```powershell
   cp .env.example .env
   ```

2. **Edita `.env` con tus valores reales:**
   ```bash
   # .env (NO subir a Git - ya está en .gitignore)
   JWT_SECRET=a7f2c9e1b4d8f3a6e9c2b5d8f1a4e7c9b2d5f8a1c4e7b9d2f5a8c1e4b7d9f2a5
   JWT_REFRESH_SECRET=b8e3d0f2c5a9e2d5f8b1c4e7a0d3f6b9c2e5a8d1f4b7c0e3a6d9f2b5c8e1a4
   JWT_ALGORITHM=HS256
   JWT_EXPIRE_MINUTES=30
   ENVIRONMENT=development
   ```

3. **Generar claves seguras (256 bits):**
   ```powershell
   # Opción 1: Python
   .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
   
   # Opción 2: PowerShell
   -join ((48..57) + (97..102) | Get-Random -Count 64 | ForEach-Object {[char]$_})
   ```

### Validaciones Automáticas

El archivo `config.py` valida automáticamente:
- ✅ JWT_SECRET tiene al menos 32 caracteres
- ✅ JWT_SECRET y JWT_REFRESH_SECRET son diferentes
- ✅ Si falta algún secreto requerido, la aplicación NO inicia

### Estructura del Sistema

```
config.py                 # Configuración centralizada con pydantic-settings
├── .env                  # Secretos REALES (gitignored)
├── .env.example          # Plantilla documentada
└── main.py               # Carga config al inicio
```

---

## 🔒 Generación de Certificados SSL

### Para Desarrollo Local

Los certificados autofirmados son perfectos para desarrollo local, pero los navegadores mostrarán una advertencia (es normal).

#### Método 1: Script Python (Recomendado)

```powershell
# Generar certificados automáticamente
.\.venv\Scripts\python.exe generar_certificados.py
```

Este script:
- ✅ Crea par de llaves RSA de 4096 bits
- ✅ Genera certificado autofirmado válido por 365 días
- ✅ Incluye Subject Alternative Names (localhost, 127.0.0.1, ecomarket.local)
- ✅ Guarda archivos en `certs/cert.pem` y `certs/key.pem`

#### Método 2: OpenSSL (Si está instalado)

```bash
# Crear directorio
mkdir certs

# Generar certificado
openssl req -x509 -newkey rsa:4096 \
  -keyout certs/key.pem \
  -out certs/cert.pem \
  -days 365 \
  -nodes \
  -subj "/CN=localhost/O=EcoMarket Dev/C=MX"
```

### Verificar Certificado

```powershell
# Ver detalles del certificado
.\.venv\Scripts\python.exe -c "from cryptography import x509; from cryptography.hazmat.primitives import serialization; cert = x509.load_pem_x509_certificate(open('certs/cert.pem', 'rb').read()); print(f'Emisor: {cert.issuer}'); print(f'Válido desde: {cert.not_valid_before_utc}'); print(f'Válido hasta: {cert.not_valid_after_utc}')"
```

### ⚠️ IMPORTANTE: Seguridad de Certificados

```gitignore
# Agregar a .gitignore (ya incluido)
*.pem
*.key
*.crt
*.pfx
*.p12
certs/
```

**NUNCA subas certificados privados a Git.** Si lo haces por error:
1. Regenera inmediatamente los certificados
2. Limpia el historial de Git o rota el repositorio

---

## 🚀 Ejecución con HTTPS

### Inicio Automático con Detección

El servidor detecta automáticamente si existen certificados:

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecutar servidor
python main.py
```

**Comportamiento:**
- ✅ **Con certificados** → Inicia en `https://localhost:8443`
- ⚠️ **Sin certificados** → Inicia en `http://localhost:8001` (modo inseguro)

### Salida del Servidor (HTTPS Habilitado)

```
======================================================================
🔒 Iniciando EcoMarket API con HTTPS (TLS/SSL)
======================================================================
📍 URL: https://localhost:8443
📄 Documentación: https://localhost:8443/docs
🔐 Certificado: certs/cert.pem
⚠️  Advertencia: Certificado autofirmado (solo desarrollo)
   Los navegadores mostrarán advertencia - es normal
======================================================================
```

### Acceso desde Navegador

1. **Abre:** `https://localhost:8443`
2. **Advertencia de seguridad:**
   - Chrome: Click en "Avanzado" → "Acceder a localhost (sitio no seguro)"
   - Firefox: Click en "Avanzado" → "Aceptar el riesgo y continuar"
   - Edge: Click en "Avanzado" → "Continuar a localhost (no seguro)"

3. **Verificar conexión segura:**
   - Busca el candado 🔒 en la barra de direcciones
   - Click en el candado → "Certificado" → Verifica emisor y validez

### Pruebas con curl

```powershell
# Opción 1: Ignorar verificación SSL (desarrollo)
curl -k https://localhost:8443/health

# Opción 2: Especificar certificado CA
curl --cacert certs/cert.pem https://localhost:8443/health

# Probar login con JWT
curl -k -X POST https://localhost:8443/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"admin@ecomarket.com\",\"password\":\"admin123\"}'
```

### Pruebas con Postman

1. **Configuración SSL:**
   - Settings → General → SSL certificate verification → **OFF** (solo desarrollo)
   
2. **Hacer request:**
   - URL: `https://localhost:8443/api/auth/login`
   - Method: `POST`
   - Body → raw → JSON:
     ```json
     {
       "email": "admin@ecomarket.com",
       "password": "admin123"
     }
     ```

---

## 🔧 Troubleshooting

### Error: "ERR_CERT_AUTHORITY_INVALID"

**Causa:** El navegador no confía en certificados autofirmados.

**Solución:**
- ✅ Es **normal** en desarrollo local
- ✅ Acepta la excepción de seguridad manualmente
- ✅ Para evitarlo, usa herramientas como `mkcert` que instalan CA local

### Error: "ssl.SSLError: [SSL] PEM lib"

**Causa:** Archivos de certificado corruptos o no encontrados.

**Solución:**
```powershell
# Regenerar certificados
rm -r certs
python generar_certificados.py

# Verificar que existen
ls certs
```

### Error: "Address already in use"

**Causa:** Puerto 8443 ocupado por otro proceso.

**Solución:**
```powershell
# Windows: Encontrar proceso usando puerto 8443
netstat -ano | findstr :8443

# Terminar proceso (reemplaza PID)
taskkill /PID <PID> /F

# Alternativa: Terminar todos los Python
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force
```

### Error: "Config keys have changed in V2: 'fields' removed"

**Causa:** Warning de compatibilidad pydantic-settings V2.

**Solución:**
- ✅ Es solo un **warning**, no afecta funcionalidad
- ✅ Se puede ignorar de manera segura
- ✅ Actualizar `config.py` si deseas eliminar el warning (usar `model_config` en lugar de `Config.fields`)

### Servidor no arranca con HTTPS

**Diagnóstico paso a paso:**

1. **Verificar certificados existen:**
   ```powershell
   Test-Path certs/cert.pem
   Test-Path certs/key.pem
   ```

2. **Verificar permisos de lectura:**
   ```powershell
   Get-Acl certs/cert.pem | Format-List
   ```

3. **Probar certificado manualmente:**
   ```powershell
   python -c "import ssl; ssl.create_default_context().load_cert_chain('certs/cert.pem', 'certs/key.pem'); print('OK')"
   ```

4. **Ver logs completos:**
   ```powershell
   python main.py 2>&1 | Tee-Object -FilePath debug.log
   ```

---

## 🏭 Producción

### ⚠️ NO usar certificados autofirmados en producción

Para producción, necesitas certificados firmados por una CA confiable.

### Opción 1: Let's Encrypt (Gratuito)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d api.ecomarket.com

# Renovación automática (cron)
0 0 1 * * certbot renew --quiet && systemctl reload nginx
```

### Opción 2: Nginx como Reverse Proxy (SSL Termination)

**Ventajas:**
- ✅ Centraliza gestión de certificados
- ✅ Reduce carga de CPU en backend
- ✅ Permite load balancing

**nginx.conf:**
```nginx
server {
    listen 443 ssl http2;
    server_name api.ecomarket.com;
    
    # Certificados de Let's Encrypt
    ssl_certificate /etc/letsencrypt/live/api.ecomarket.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.ecomarket.com/privkey.pem;
    
    # TLS moderno
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    location / {
        proxy_pass http://localhost:8000;  # Backend sin TLS
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirección HTTP → HTTPS
server {
    listen 80;
    server_name api.ecomarket.com;
    return 301 https://$server_name$request_uri;
}
```

### Opción 3: Cloud Providers

#### AWS
- **ACM (AWS Certificate Manager):** Certificados gratuitos para ELB/CloudFront
- **Integración:** ALB con auto-renovación

#### Azure
- **Azure Key Vault:** Gestión centralizada de certificados
- **App Service:** Certificados gestionados incluidos

#### Google Cloud
- **Cloud Load Balancing:** Certificados SSL gestionados automáticamente

### Variables de Entorno en Producción

```bash
# .env (producción - usar secrets manager)
ENVIRONMENT=production
JWT_SECRET=<clave-ultra-segura-producción>
JWT_REFRESH_SECRET=<otra-clave-diferente-producción>
DB_URL=postgresql://user:pass@db.example.com:5432/ecomarket_prod
```

**IMPORTANTE:**
- 🚫 NO usar archivos `.env` en servidores de producción
- ✅ Usar AWS Secrets Manager, Azure Key Vault, o HashiCorp Vault
- ✅ Rotar secretos cada 90 días como mínimo
- ✅ Configurar alertas de expiración de certificados

### Checklist de Producción

- [ ] Certificados firmados por CA confiable (Let's Encrypt, DigiCert, etc.)
- [ ] HSTS habilitado (`Strict-Transport-Security` header)
- [ ] TLS 1.2+ (deshabilitar TLS 1.0/1.1)
- [ ] Redirección HTTP → HTTPS activa
- [ ] Secretos en secrets manager (no en .env)
- [ ] Monitoreo de expiración de certificados
- [ ] Renovación automática configurada
- [ ] Logs de acceso y errores SSL
- [ ] Rate limiting y WAF configurados

---

## 📊 Comparación: HTTP vs HTTPS

| Aspecto | HTTP (❌ Inseguro) | HTTPS (✅ Seguro) |
|---------|-------------------|-------------------|
| **Confidencialidad** | Datos en texto plano | Datos cifrados (TLS) |
| **Integridad** | Puede ser modificado | Firma digital verifica integridad |
| **Autenticación** | Sin verificación de servidor | Certificado valida identidad del servidor |
| **Protección MITM** | ❌ Vulnerable | ✅ Protegido |
| **SEO** | ❌ Penalizado por Google | ✅ Preferido por buscadores |
| **Navegadores** | ⚠️ "No seguro" | ✅ Candado 🔒 |
| **Compliance** | ❌ No cumple GDPR/PCI-DSS | ✅ Requisito obligatorio |

---

## 🔗 Recursos Adicionales

### Documentación Oficial
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Uvicorn SSL](https://www.uvicorn.org/#deployment)
- [Let's Encrypt](https://letsencrypt.org/getting-started/)
- [Mozilla SSL Config Generator](https://ssl-config.mozilla.org/)

### Herramientas de Testing
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/) - Analiza configuración SSL
- [Security Headers](https://securityheaders.com/) - Verifica headers de seguridad
- [Hardenize](https://www.hardenize.com/) - Auditoría completa de TLS

### Mejores Prácticas
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [The Twelve-Factor App](https://12factor.net/) - Factor III: Config
- [NIST Cryptographic Standards](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)

---

## 📝 Resumen de Comandos

```powershell
# 1. Configurar secretos
cp .env.example .env
# Editar .env con valores reales

# 2. Generar certificados
python generar_certificados.py

# 3. Iniciar servidor con HTTPS
python main.py

# 4. Probar
curl -k https://localhost:8443/health

# 5. Acceder en navegador
# https://localhost:8443 (aceptar advertencia de certificado)
```

---

<div align="center">

### 🔒 Sistema Seguro Implementado

**JWT (Semana 8)** + **HTTPS (Semana 9)** + **Secretos Externalizados**

✅ Autenticación | ✅ Cifrado | ✅ Configuración Segura

</div>
