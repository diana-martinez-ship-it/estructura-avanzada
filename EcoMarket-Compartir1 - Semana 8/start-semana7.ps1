# 🚀 Script de Inicio Rápido - Semana 7: Replicación y Sharding
# Levanta toda la infraestructura y ejecuta pruebas

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   ECOMARKET - REPLICACIÓN Y SHARDING" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Paso 1: Instalar dependencias
Write-Host "📦 Paso 1: Instalando dependencias Python..." -ForegroundColor Yellow
pip install -q psycopg2-binary asyncpg

# Paso 2: Limpiar contenedores anteriores
Write-Host "`n🧹 Paso 2: Limpiando contenedores anteriores..." -ForegroundColor Yellow
docker-compose -f docker-compose-replicacion.yml down -v 2>$null

# Paso 3: Levantar infraestructura
Write-Host "`n🐳 Paso 3: Levantando infraestructura (esto puede tardar 2-3 min)..." -ForegroundColor Yellow
docker-compose -f docker-compose-replicacion.yml up -d --build

# Paso 4: Esperar a que se inicialicen
Write-Host "`n⏳ Paso 4: Esperando inicialización de PostgreSQL..." -ForegroundColor Yellow
Write-Host "   (Primario + réplicas haciendo pg_basebackup inicial)" -ForegroundColor Gray

Start-Sleep -Seconds 60

# Verificar estado
Write-Host "`n✅ Verificando contenedores..." -ForegroundColor Green
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Paso 5: Ejecutar pruebas
Write-Host "`n🧪 Paso 5: Ejecutando suite de pruebas..." -ForegroundColor Yellow
Write-Host "   (6 pruebas: replicación, distribución, lag, sharding)`n" -ForegroundColor Gray

python test_replication_sharding.py

# Resumen final
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   ✅ SISTEMA LISTO" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "🌐 Endpoints disponibles:" -ForegroundColor White
Write-Host "  • API (Load Balanced): http://localhost" -ForegroundColor Gray
Write-Host "  • API Instancia 1: http://localhost:8001" -ForegroundColor Gray
Write-Host "  • API Instancia 2: http://localhost:8002" -ForegroundColor Gray
Write-Host "  • RabbitMQ Management: http://localhost:15672" -ForegroundColor Gray
Write-Host "`n  • PostgreSQL Primary: localhost:5432" -ForegroundColor Gray
Write-Host "  • PostgreSQL Standby-1: localhost:5433" -ForegroundColor Gray
Write-Host "  • PostgreSQL Standby-2: localhost:5434" -ForegroundColor Gray

Write-Host "`n🔍 Comandos útiles:" -ForegroundColor White
Write-Host "  docker logs postgres-primary         # Ver logs del primario" -ForegroundColor Gray
Write-Host "  docker logs postgres-standby-1       # Ver logs réplica 1" -ForegroundColor Gray
Write-Host "  python shard_router.py               # Demo de sharding" -ForegroundColor Gray
Write-Host "  python test_replication_sharding.py  # Re-ejecutar pruebas`n" -ForegroundColor Gray

Write-Host "📚 Documentación: README-SEMANA7.md`n" -ForegroundColor Cyan
