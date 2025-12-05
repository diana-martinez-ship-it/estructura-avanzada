# 🎬 DEMO SIMPLE - Balanceo de Carga
Write-Host "`n=== DEMO BALANCEO DE CARGA ===" -ForegroundColor Cyan

# 1. Verificar RabbitMQ
Write-Host "`n1. Verificando RabbitMQ..." -ForegroundColor Yellow
docker start rabbitmq-ecomarket 2>$null
Start-Sleep -Seconds 2

# 2. Iniciar Instancia 1
Write-Host "2. Iniciando Instancia 1 (Puerto 8001)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit -Command `$env:INSTANCE_ID='1'; `$env:RABBITMQ_HOST='localhost'; python -m uvicorn main:app --port 8001"
Start-Sleep -Seconds 4

# 3. Iniciar Instancia 2
Write-Host "3. Iniciando Instancia 2 (Puerto 8002)..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit -Command `$env:INSTANCE_ID='2'; `$env:RABBITMQ_HOST='localhost'; python -m uvicorn main:app --port 8002"
Start-Sleep -Seconds 4

Write-Host "`n=== SISTEMA LISTO ===" -ForegroundColor Green
Write-Host "Instancia 1: http://localhost:8001" -ForegroundColor Green
Write-Host "Instancia 2: http://localhost:8002`n" -ForegroundColor Blue

# 4. Probar balanceo
Write-Host "4. PROBANDO BALANCEO (10 requests)...`n" -ForegroundColor Yellow

1..10 | ForEach-Object {
    $puerto = if ($_ % 2) { 8001 } else { 8002 }
    $color = if ($_ % 2) { "Green" } else { "Blue" }
    
    try {
        $resp = Invoke-RestMethod "http://localhost:$puerto/health"
        Write-Host "   Request #$_ -> Instancia $($resp.instance_id)" -ForegroundColor $color
    } catch {
        Write-Host "   Request #$_ -> Error" -ForegroundColor Red
    }
    Start-Sleep -Milliseconds 500
}

Write-Host "`n=== DEMO COMPLETADA ===" -ForegroundColor Green
Write-Host "Cierra las ventanas de PowerShell para detener las instancias`n"
