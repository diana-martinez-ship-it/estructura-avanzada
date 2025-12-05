# Copia y pega esto despues de cerrar una instancia:

Write-Host "`n===========================================" -ForegroundColor Yellow
Write-Host "  DEMO: RESILIENCIA DEL SISTEMA" -ForegroundColor Yellow
Write-Host "===========================================`n" -ForegroundColor Yellow

Write-Host "Probando ambas instancias...`n" -ForegroundColor White

$inst1_ok = $false
$inst2_ok = $false

try {
    $null = Invoke-RestMethod "http://localhost:8001/health" -TimeoutSec 2
    $inst1_ok = $true
    Write-Host "  [OK] Instancia 1: ACTIVA" -ForegroundColor Green
} catch {
    Write-Host "  [X] Instancia 1: CAIDA" -ForegroundColor Red
}

try {
    $null = Invoke-RestMethod "http://localhost:8002/health" -TimeoutSec 2
    $inst2_ok = $true
    Write-Host "  [OK] Instancia 2: ACTIVA" -ForegroundColor Green
} catch {
    Write-Host "  [X] Instancia 2: CAIDA" -ForegroundColor Red
}

Write-Host ""

if ($inst1_ok -or $inst2_ok) {
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "  SISTEMA RESILIENTE!" -ForegroundColor Green
    Write-Host "  El sistema sigue funcionando" -ForegroundColor Green
    Write-Host "  aunque una instancia fallo" -ForegroundColor Green
    Write-Host "============================================`n" -ForegroundColor Green
} else {
    Write-Host "  Ambas instancias estan caidas`n" -ForegroundColor Yellow
}
