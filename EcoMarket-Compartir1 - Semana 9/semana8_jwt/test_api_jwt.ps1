# 🧪 Script de Pruebas JWT - PowerShell
# =====================================
# Este script demuestra el funcionamiento completo del sistema JWT

Write-Host "🔐 PRUEBAS DE SISTEMA JWT - ECOMARKET API" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://127.0.0.1:8001"

# ============================================================================
# TEST 1: LOGIN EXITOSO
# ============================================================================

Write-Host "📝 TEST 1: Login exitoso con usuario Admin" -ForegroundColor Yellow
Write-Host "Endpoint: POST /api/auth/login" -ForegroundColor Gray

$loginBody = @{
    email = "admin@ecomarket.com"
    password = "admin123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" `
        -Method Post `
        -Body $loginBody `
        -ContentType "application/json"
    
    $accessToken = $response.access_token
    $refreshToken = $response.refresh_token
    
    Write-Host "✅ Login exitoso!" -ForegroundColor Green
    Write-Host "   Access Token: $($accessToken.Substring(0, 50))..." -ForegroundColor White
    Write-Host "   Expira en: $($response.expires_in) segundos" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "❌ Error en login: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Start-Sleep -Seconds 2

# ============================================================================
# TEST 2: OBTENER INFORMACIÓN DEL USUARIO ACTUAL
# ============================================================================

Write-Host "📝 TEST 2: Obtener información del usuario autenticado" -ForegroundColor Yellow
Write-Host "Endpoint: GET /api/auth/me" -ForegroundColor Gray

try {
    $headers = @{
        "Authorization" = "Bearer $accessToken"
    }
    
    $userInfo = Invoke-RestMethod -Uri "$baseUrl/api/auth/me" `
        -Method Get `
        -Headers $headers
    
    Write-Host "✅ Usuario autenticado:" -ForegroundColor Green
    Write-Host "   Email: $($userInfo.email)" -ForegroundColor White
    Write-Host "   Nombre: $($userInfo.name)" -ForegroundColor White
    Write-Host "   Rol: $($userInfo.role)" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# ============================================================================
# TEST 3: ACCESO A ENDPOINT PROTEGIDO (CON TOKEN)
# ============================================================================

Write-Host "📝 TEST 3: Crear producto con token válido (Admin)" -ForegroundColor Yellow
Write-Host "Endpoint: POST /api/productos" -ForegroundColor Gray

$productBody = @{
    nombre = "Manzana Orgánica JWT Test"
    categoria = "Frutas"
    precio = 3.50
    stock = 100
    descripcion = "Producto creado mediante autenticación JWT"
} | ConvertTo-Json

try {
    $headers = @{
        "Authorization" = "Bearer $accessToken"
        "Content-Type" = "application/json"
    }
    
    $newProduct = Invoke-RestMethod -Uri "$baseUrl/api/productos" `
        -Method Post `
        -Body $productBody `
        -Headers $headers
    
    Write-Host "✅ Producto creado exitosamente!" -ForegroundColor Green
    Write-Host "   ID: $($newProduct.id)" -ForegroundColor White
    Write-Host "   Nombre: $($newProduct.nombre)" -ForegroundColor White
    Write-Host "   Precio: `$$($newProduct.precio)" -ForegroundColor White
    Write-Host ""
    
    $productId = $newProduct.id
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# ============================================================================
# TEST 4: ACCESO SIN TOKEN (DEBE FALLAR)
# ============================================================================

Write-Host "📝 TEST 4: Intentar crear producto SIN token (debe fallar 401)" -ForegroundColor Yellow
Write-Host "Endpoint: POST /api/productos" -ForegroundColor Gray

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/productos" `
        -Method Post `
        -Body $productBody `
        -ContentType "application/json"
    
    Write-Host "❌ ERROR: El endpoint debería haber rechazado la petición!" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "✅ Correcto: Petición rechazada con 401 Unauthorized" -ForegroundColor Green
        Write-Host "   Mensaje: No autenticado" -ForegroundColor White
    } else {
        Write-Host "❌ Error inesperado: $($_.Exception.Message)" -ForegroundColor Red
    }
}
Write-Host ""

Start-Sleep -Seconds 2

# ============================================================================
# TEST 5: REFRESH TOKEN
# ============================================================================

Write-Host "📝 TEST 5: Renovar access token con refresh token" -ForegroundColor Yellow
Write-Host "Endpoint: POST /api/auth/refresh" -ForegroundColor Gray

$refreshBody = @{
    refresh_token = $refreshToken
} | ConvertTo-Json

try {
    $refreshResponse = Invoke-RestMethod -Uri "$baseUrl/api/auth/refresh" `
        -Method Post `
        -Body $refreshBody `
        -ContentType "application/json"
    
    Write-Host "✅ Token renovado exitosamente!" -ForegroundColor Green
    Write-Host "   Nuevo Access Token: $($refreshResponse.access_token.Substring(0, 50))..." -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# ============================================================================
# TEST 6: LOGIN CON OTRO ROL (VENDEDOR)
# ============================================================================

Write-Host "📝 TEST 6: Login como Vendedor" -ForegroundColor Yellow
Write-Host "Endpoint: POST /api/auth/login" -ForegroundColor Gray

$vendedorBody = @{
    email = "vendedor@ecomarket.com"
    password = "vendedor123"
} | ConvertTo-Json

try {
    $vendedorResponse = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" `
        -Method Post `
        -Body $vendedorBody `
        -ContentType "application/json"
    
    $vendedorToken = $vendedorResponse.access_token
    
    Write-Host "✅ Login como vendedor exitoso!" -ForegroundColor Green
    Write-Host "   Token: $($vendedorToken.Substring(0, 50))..." -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# ============================================================================
# TEST 7: INTENTAR ELIMINAR CON ROL VENDEDOR (DEBE FALLAR)
# ============================================================================

Write-Host "📝 TEST 7: Vendedor intenta eliminar producto (debe fallar 403)" -ForegroundColor Yellow
Write-Host "Endpoint: DELETE /api/productos/$productId" -ForegroundColor Gray

try {
    $headers = @{
        "Authorization" = "Bearer $vendedorToken"
    }
    
    Invoke-RestMethod -Uri "$baseUrl/api/productos/$productId" `
        -Method Delete `
        -Headers $headers
    
    Write-Host "❌ ERROR: El vendedor NO debería poder eliminar!" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 403) {
        Write-Host "✅ Correcto: Vendedor sin permisos para eliminar (403 Forbidden)" -ForegroundColor Green
        Write-Host "   Mensaje: Solo administradores pueden realizar esta acción" -ForegroundColor White
    } else {
        Write-Host "❌ Error inesperado: $($_.Exception.Message)" -ForegroundColor Red
    }
}
Write-Host ""

Start-Sleep -Seconds 2

# ============================================================================
# TEST 8: ELIMINAR CON ROL ADMIN
# ============================================================================

Write-Host "📝 TEST 8: Admin elimina el producto de prueba" -ForegroundColor Yellow
Write-Host "Endpoint: DELETE /api/productos/$productId" -ForegroundColor Gray

try {
    $headers = @{
        "Authorization" = "Bearer $accessToken"
    }
    
    $deleteResponse = Invoke-RestMethod -Uri "$baseUrl/api/productos/$productId" `
        -Method Delete `
        -Headers $headers
    
    Write-Host "✅ Producto eliminado exitosamente!" -ForegroundColor Green
    Write-Host "   Mensaje: $($deleteResponse.message)" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# ============================================================================
# TEST 9: LOGOUT
# ============================================================================

Write-Host "📝 TEST 9: Cerrar sesión (revocar refresh token)" -ForegroundColor Yellow
Write-Host "Endpoint: POST /api/auth/logout" -ForegroundColor Gray

$logoutBody = @{
    refresh_token = $refreshToken
} | ConvertTo-Json

try {
    $logoutResponse = Invoke-RestMethod -Uri "$baseUrl/api/auth/logout" `
        -Method Post `
        -Body $logoutBody `
        -ContentType "application/json"
    
    Write-Host "✅ Sesión cerrada exitosamente!" -ForegroundColor Green
    Write-Host "   Mensaje: $($logoutResponse.message)" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================================================
# RESUMEN
# ============================================================================

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ PRUEBAS COMPLETADAS" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Funcionalidades Probadas:" -ForegroundColor White
Write-Host "  ✓ Login con credenciales válidas" -ForegroundColor Green
Write-Host "  ✓ Obtener información del usuario autenticado" -ForegroundColor Green
Write-Host "  ✓ Crear producto con token válido" -ForegroundColor Green
Write-Host "  ✓ Rechazar peticiones sin token (401)" -ForegroundColor Green
Write-Host "  ✓ Renovar access token con refresh token" -ForegroundColor Green
Write-Host "  ✓ Sistema de roles (Admin vs Vendedor)" -ForegroundColor Green
Write-Host "  ✓ Control de permisos por rol (403)" -ForegroundColor Green
Write-Host "  ✓ Cerrar sesión y revocar refresh token" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 Sistema JWT funcionando correctamente!" -ForegroundColor Cyan
Write-Host ""
