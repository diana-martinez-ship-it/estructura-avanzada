# 🚀 Guía de Inicio Rápido - EcoMarket Load Balancing

## ⚡ Inicio Rápido (5 minutos)

### 1. Levantar Todo el Sistema

```powershell
# Construir y levantar todos los servicios
docker-compose up -d --build

# Verificar que todo está corriendo
docker ps
```

**Deberías ver 4 contenedores:**
- ✅ `nginx-loadbalancer`
- ✅ `ecomarket-api-1`
- ✅ `ecomarket-api-2`
- ✅ `rabbitmq-ecomarket`

### 2. Probar el Balanceo Inmediatamente

```powershell
# Test rápido - 10 requests
for ($i=1; $i -le 10; $i++) { 
    $response = Invoke-RestMethod http://localhost/health
    Write-Host "Request #$i -> Instancia $($response.instance_id)" -ForegroundColor $(if ($response.instance_id -eq "1") {"Green"} else {"Blue"})
}
```

**Resultado Esperado:**
```
Request #1 -> Instancia 1
Request #2 -> Instancia 2
Request #3 -> Instancia 1
Request #4 -> Instancia 2
...
```

### 3. Abrir la Interfaz Web

```powershell
# Abrir en el navegador
start http://localhost/
```

## 🧪 Pruebas Interactivas

### Opción A: Script Automatizado (Recomendado)

```powershell
# Ejecutar script de pruebas interactivo
.\test-loadbalancer.ps1
```

**Menú Interactivo:**
1. Verificar estado de contenedores
2. Prueba básica de balanceo (10 requests)
3. Prueba intensiva de balanceo (50 requests)
4. Prueba de resiliencia (con fallo de instancia)
5. Ver logs en tiempo real
6. Ver métricas de Nginx
7. Acceder a instancia específica

### Opción B: Comandos Manuales

#### Ver Distribución de Carga

```powershell
# Enviar 50 requests y contar distribución
$instancias = @{}
for ($i=1; $i -le 50; $i++) {
    $r = Invoke-RestMethod http://localhost/health
    $instancias[$r.instance_id]++
}
$instancias
```

#### Probar Resiliencia

```powershell
# Terminal 1: Flood constante
while ($true) { 
    try { Invoke-RestMethod http://localhost/health | Out-Null; Write-Host "✅" -NoNewline } 
    catch { Write-Host "❌" -NoNewline }
    Start-Sleep -Milliseconds 500 
}

# Terminal 2: Detener instancia
docker stop ecomarket-api-1
# Observa que no hay errores en Terminal 1

# Reiniciar instancia
docker start ecomarket-api-1
```

#### Ver Logs en Tiempo Real

```powershell
# Ver todos los logs
docker-compose logs -f

# Ver log de una instancia específica
docker logs -f ecomarket-api-1

# Ver solo logs de Nginx
docker logs -f nginx-loadbalancer
```

## 📊 Verificar Métricas

### Métricas de Nginx

```powershell
# Ver estadísticas de conexiones
Invoke-RestMethod http://localhost:8080/nginx_status
```

**Output:**
```
Active connections: 2
server accepts handled requests
 342 342 456
Reading: 0 Writing: 1 Waiting: 1
```

### Health Check de Instancias

```powershell
# A través del load balancer
Invoke-RestMethod http://localhost/health

# Directamente a cada instancia
Invoke-RestMethod http://localhost:8001/health  # Instancia 1
Invoke-RestMethod http://localhost:8002/health  # Instancia 2
```

## 🛠️ Comandos Útiles

### Gestión de Contenedores

```powershell
# Ver estado
docker ps

# Ver recursos (CPU, RAM)
docker stats

# Reiniciar un servicio
docker restart ecomarket-api-1

# Ver logs con timestamp
docker logs -f --timestamps ecomarket-api-1

# Detener todo
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

### Debugging

```powershell
# Entrar a un contenedor
docker exec -it ecomarket-api-1 bash

# Ver configuración de Nginx
docker exec nginx-loadbalancer cat /etc/nginx/nginx.conf

# Recargar configuración de Nginx sin downtime
docker exec nginx-loadbalancer nginx -s reload

# Test de configuración de Nginx
docker exec nginx-loadbalancer nginx -t
```

## 🔥 Pruebas de Carga

### Con Curl (Básico)

```powershell
# 100 requests secuenciales
for ($i=1; $i -le 100; $i++) {
    curl http://localhost/health
}
```

### Con Apache Bench (Avanzado)

```powershell
# Instalar Apache Bench (si no lo tienes)
# choco install apache-httpd

# 1000 requests, 100 concurrentes
ab -n 1000 -c 100 http://localhost/health

# Ver reporte detallado
ab -n 1000 -c 100 -g results.tsv http://localhost/health
```

### Con Invoke-WebRequest (PowerShell)

```powershell
# Medir tiempo de respuesta
Measure-Command { 
    1..100 | ForEach-Object {
        Invoke-RestMethod http://localhost/health
    }
}
```

## 🎯 Casos de Uso Comunes

### 1. Agregar una Tercera Instancia

```powershell
# 1. Editar docker-compose.yml y descomentar instancia 3

# 2. Levantar la nueva instancia
docker-compose up -d ecomarket-api-3

# 3. Actualizar Nginx config (agregar server api-3:8000)

# 4. Recargar Nginx
docker exec nginx-loadbalancer nginx -s reload

# 5. Verificar distribución
for ($i=1; $i -le 30; $i++) {
    $r = Invoke-RestMethod http://localhost/health
    Write-Host "Request #$i -> Instancia $($r.instance_id)"
}
```

### 2. Simular Fallo y Recuperación

```powershell
# Flood de requests
$job = Start-Job {
    while ($true) {
        Invoke-RestMethod http://localhost/health | Out-Null
        Start-Sleep -Milliseconds 200
    }
}

# Detener instancia
docker stop ecomarket-api-1
Start-Sleep 5

# Reiniciar instancia
docker start ecomarket-api-1
Start-Sleep 10

# Ver logs
docker logs ecomarket-api-2 --tail 20

# Detener flood
Stop-Job $job; Remove-Job $job
```

### 3. Monitoreo Continuo

```powershell
# Script de monitoreo simple
while ($true) {
    Clear-Host
    Write-Host "=== ECOMARKET MONITORING ===" -ForegroundColor Green
    Write-Host ""
    
    # Estado de contenedores
    Write-Host "Contenedores:" -ForegroundColor Cyan
    docker ps --format "table {{.Names}}\t{{.Status}}"
    
    Write-Host ""
    
    # Health checks
    Write-Host "Health Checks:" -ForegroundColor Cyan
    try {
        $h1 = Invoke-RestMethod http://localhost:8001/health
        Write-Host "  Instancia 1: ✅ OK" -ForegroundColor Green
    } catch {
        Write-Host "  Instancia 1: ❌ DOWN" -ForegroundColor Red
    }
    
    try {
        $h2 = Invoke-RestMethod http://localhost:8002/health
        Write-Host "  Instancia 2: ✅ OK" -ForegroundColor Green
    } catch {
        Write-Host "  Instancia 2: ❌ DOWN" -ForegroundColor Red
    }
    
    Start-Sleep 5
}
```

## 🚨 Troubleshooting

### Problema: Puerto 80 ya en uso

```powershell
# Ver qué proceso usa el puerto
netstat -ano | findstr :80

# Cambiar puerto en docker-compose.yml
ports:
  - "8080:80"  # Usa puerto 8080 en lugar de 80
```

### Problema: Contenedores no inician

```powershell
# Ver logs de error
docker-compose logs

# Reconstruir desde cero
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Nginx no encuentra instancias

```powershell
# Verificar red de Docker
docker network ls
docker network inspect ecomarket-compartir1_ecomarket-network

# Verificar que instancias están en la red
docker inspect ecomarket-api-1 | Select-String "Networks"
```

## 📚 Recursos Adicionales

- **README Principal:** `README-LOADBALANCER.md`
- **Informe Completo:** `INFORME-ESCALABILIDAD.md`
- **Diagramas:** `diagramas-arquitectura.html`
- **Script de Pruebas:** `test-loadbalancer.ps1`

## ✅ Checklist de Validación

- [ ] ✅ Todos los contenedores levantados
- [ ] ✅ Health checks responden
- [ ] ✅ Distribución 50/50 entre instancias
- [ ] ✅ Sistema sobrevive a caída de instancia
- [ ] ✅ Recuperación automática funciona
- [ ] ✅ Interfaz web accesible
- [ ] ✅ Logs muestran INSTANCE_ID
- [ ] ✅ RabbitMQ accesible

## 🎉 ¡Éxito!

Si completaste todos los pasos, tu sistema de balanceo de carga está funcionando correctamente. Ahora puedes:

1. **Experimentar:** Agrega más instancias, cambia algoritmos
2. **Optimizar:** Ajusta timeouts, max_fails según tu carga
3. **Monitorear:** Implementa Prometheus + Grafana
4. **Escalar:** Migra a Kubernetes para auto-scaling

---

**¿Problemas?** Revisa los logs: `docker-compose logs -f`  
**¿Preguntas?** Consulta el informe completo: `INFORME-ESCALABILIDAD.md`
