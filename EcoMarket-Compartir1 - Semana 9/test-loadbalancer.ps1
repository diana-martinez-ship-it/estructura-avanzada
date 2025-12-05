# 🧪 Script de Pruebas para Balanceo de Carga - EcoMarket
# PowerShell Script

Write-Host "🌿 ========================================" -ForegroundColor Green
Write-Host "   ECOMARKET - PRUEBAS DE LOAD BALANCING" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

# Función para hacer requests y mostrar la instancia que responde
function Test-LoadBalancing {
    param(
        [int]$NumRequests = 10,
        [string]$Endpoint = "http://localhost/health"
    )
    
    Write-Host "📊 Enviando $NumRequests requests a $Endpoint..." -ForegroundColor Cyan
    Write-Host "-------------------------------------------`n"
    
    $instancias = @{}
    
    for ($i = 1; $i -le $NumRequests; $i++) {
        try {
            $response = Invoke-RestMethod -Uri $Endpoint -Method Get -TimeoutSec 5
            $instanceId = $response.instance_id
            
            # Contar instancias
            if ($instancias.ContainsKey($instanceId)) {
                $instancias[$instanceId]++
            } else {
                $instancias[$instanceId] = 1
            }
            
            Write-Host "Request #$i -> Instancia $instanceId" -ForegroundColor $(
                if ($instanceId -eq "1") { "Green" }
                elseif ($instanceId -eq "2") { "Blue" }
                else { "Yellow" }
            )
            
            Start-Sleep -Milliseconds 200
        }
        catch {
            Write-Host "Request #$i -> ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    Write-Host "`n-------------------------------------------"
    Write-Host "📈 RESUMEN DE DISTRIBUCIÓN:" -ForegroundColor Cyan
    foreach ($key in $instancias.Keys | Sort-Object) {
        $porcentaje = [math]::Round(($instancias[$key] / $NumRequests) * 100, 1)
        Write-Host "   Instancia $key : $($instancias[$key]) requests ($porcentaje%)" -ForegroundColor White
    }
    Write-Host "-------------------------------------------`n"
}

# Función para verificar estado de contenedores
function Test-ContainersStatus {
    Write-Host "🐳 Verificando estado de contenedores..." -ForegroundColor Cyan
    Write-Host "-------------------------------------------"
    
    $containers = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | Select-Object -Skip 1
    
    if ($containers) {
        Write-Host $containers
        Write-Host "-------------------------------------------`n" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ No se encontraron contenedores activos" -ForegroundColor Red
        Write-Host "Ejecuta: docker-compose up -d`n" -ForegroundColor Yellow
        return $false
    }
}

# Función para probar resiliencia (fallo de instancia)
function Test-Resilience {
    Write-Host "🛡️ PRUEBA DE RESILIENCIA" -ForegroundColor Magenta
    Write-Host "-------------------------------------------"
    
    Write-Host "`n1️⃣ Enviando requests iniciales (10)..."
    Test-LoadBalancing -NumRequests 10
    
    Write-Host "`n2️⃣ Deteniendo Instancia 1..." -ForegroundColor Yellow
    docker stop ecomarket-api-1 | Out-Null
    Start-Sleep -Seconds 3
    
    Write-Host "`n3️⃣ Enviando requests con instancia caída (10)..."
    Test-LoadBalancing -NumRequests 10
    
    Write-Host "`n4️⃣ Reiniciando Instancia 1..." -ForegroundColor Green
    docker start ecomarket-api-1 | Out-Null
    Start-Sleep -Seconds 5
    
    Write-Host "`n5️⃣ Enviando requests con todas las instancias (10)..."
    Test-LoadBalancing -NumRequests 10
    
    Write-Host "✅ Prueba de resiliencia completada`n" -ForegroundColor Green
}

# Función para ver logs en tiempo real
function Show-Logs {
    param([string]$Container = "all")
    
    if ($Container -eq "all") {
        Write-Host "📜 Mostrando logs de todos los contenedores (Ctrl+C para salir)..." -ForegroundColor Cyan
        docker-compose logs -f
    } else {
        Write-Host "📜 Mostrando logs de $Container (Ctrl+C para salir)..." -ForegroundColor Cyan
        docker logs -f $Container
    }
}

# Menú principal
function Show-Menu {
    Write-Host "`n🔧 MENÚ DE PRUEBAS" -ForegroundColor Yellow
    Write-Host "==================" -ForegroundColor Yellow
    Write-Host "1. Verificar estado de contenedores"
    Write-Host "2. Prueba básica de balanceo (10 requests)"
    Write-Host "3. Prueba intensiva de balanceo (50 requests)"
    Write-Host "4. Prueba de resiliencia (con fallo de instancia)"
    Write-Host "5. Ver logs en tiempo real"
    Write-Host "6. Ver métricas de Nginx"
    Write-Host "7. Acceder a instancia específica"
    Write-Host "0. Salir"
    Write-Host "==================`n" -ForegroundColor Yellow
}

# Loop principal
do {
    Show-Menu
    $opcion = Read-Host "Selecciona una opción"
    
    switch ($opcion) {
        "1" {
            Test-ContainersStatus
            Read-Host "Presiona Enter para continuar"
        }
        "2" {
            if (Test-ContainersStatus) {
                Test-LoadBalancing -NumRequests 10
            }
            Read-Host "Presiona Enter para continuar"
        }
        "3" {
            if (Test-ContainersStatus) {
                Test-LoadBalancing -NumRequests 50
            }
            Read-Host "Presiona Enter para continuar"
        }
        "4" {
            if (Test-ContainersStatus) {
                Test-Resilience
            }
            Read-Host "Presiona Enter para continuar"
        }
        "5" {
            Write-Host "`nSelecciona contenedor:"
            Write-Host "1. Todos"
            Write-Host "2. Nginx"
            Write-Host "3. Instancia 1"
            Write-Host "4. Instancia 2"
            $logChoice = Read-Host "Opción"
            
            switch ($logChoice) {
                "1" { Show-Logs -Container "all" }
                "2" { Show-Logs -Container "nginx-loadbalancer" }
                "3" { Show-Logs -Container "ecomarket-api-1" }
                "4" { Show-Logs -Container "ecomarket-api-2" }
            }
        }
        "6" {
            Write-Host "`n📊 Métricas de Nginx:" -ForegroundColor Cyan
            try {
                $metrics = Invoke-RestMethod -Uri "http://localhost:8080/nginx_status"
                Write-Host $metrics -ForegroundColor White
            }
            catch {
                Write-Host "❌ No se pudieron obtener las métricas" -ForegroundColor Red
            }
            Read-Host "Presiona Enter para continuar"
        }
        "7" {
            Write-Host "`nAcceder a instancia:"
            Write-Host "1. Instancia 1 (8001)"
            Write-Host "2. Instancia 2 (8002)"
            $instanceChoice = Read-Host "Opción"
            
            $port = if ($instanceChoice -eq "1") { "8001" } else { "8002" }
            $url = "http://localhost:$port/health"
            
            Write-Host "`n🔗 Accediendo a $url..." -ForegroundColor Cyan
            try {
                $response = Invoke-RestMethod -Uri $url
                Write-Host ($response | ConvertTo-Json) -ForegroundColor Green
            }
            catch {
                Write-Host "❌ Error al acceder: $($_.Exception.Message)" -ForegroundColor Red
            }
            Read-Host "Presiona Enter para continuar"
        }
        "0" {
            Write-Host "`n👋 ¡Hasta luego!" -ForegroundColor Green
        }
        default {
            Write-Host "`n❌ Opción inválida" -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
} while ($opcion -ne "0")
