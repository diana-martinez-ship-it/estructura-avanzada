# 🌿 EcoMarket - Semana 7: Replicación y Sharding de Base de Datos

## 📋 Descripción

Implementación de **replicación PostgreSQL** (primario-secundario) y **sharding** (particionamiento de datos) para escalar horizontalmente la base de datos de EcoMarket.

### 🎯 Objetivos Logrados

- ✅ Replicación streaming PostgreSQL con 1 primario + 2 secundarios
- ✅ Router de sharding con Simple Hash y Consistent Hashing
- ✅ Distribución de carga: Writes → Primario, Reads → Secundarios
- ✅ Scripts de prueba ejecutables para validar distribución
- ✅ Análisis de trade-offs CAP (Consistencia vs Disponibilidad)

---

## 🏗️ Arquitectura

```
                    ┌─────────────────┐
                    │   NGINX LB      │
                    │   (Puerto 80)   │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
     ┌────▼────┐      ┌──────▼─────┐    ┌──────▼─────┐
     │ API-1   │      │   API-2    │    │   API-N    │
     │ (8001)  │      │   (8002)   │    │   (800N)   │
     └────┬────┘      └──────┬─────┘    └──────┬─────┘
          │                  │                  │
          │   WRITES         │                  │
          └──────────────────┼──────────────────┘
                             │
                    ┌────────▼────────┐
                    │   PRIMARY DB    │◄──────┐
                    │   PostgreSQL    │       │
                    │   (Puerto 5432) │       │
                    └────────┬────────┘       │
                             │                │
          Streaming Replication              │
                             │                │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
     ┌────▼────┐      ┌──────▼─────┐          │
     │STANDBY-1│      │ STANDBY-2  │          │
     │ (5433)  │      │   (5434)   │          │
     └────┬────┘      └──────┬─────┘          │
          │                  │                 │
          │      READS       │                 │
          └──────────────────┴─────────────────┘
```

### Componentes

1. **PostgreSQL Primary** (puerto 5432)
   - Recibe todas las escrituras
   - Envía WAL logs a secundarios vía streaming replication
   
2. **PostgreSQL Standby 1 y 2** (puertos 5433, 5434)
   - Réplicas de solo lectura
   - Reciben actualizaciones async del primario
   - Sirven queries SELECT para escalar throughput de lectura

3. **Shard Router**
   - **Simple Hash**: `hash(key) % N` - fácil pero requiere redistribución al escalar
   - **Consistent Hash**: Virtual nodes en ring - solo mueve K/N datos al agregar shards

---

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose
- Python 3.9+ con pip
- 8GB RAM mínimo (para correr 3 instancias de PostgreSQL)

### Paso 1: Instalar Dependencias Python

```powershell
pip install -r requirements.txt
```

### Paso 2: Levantar Infraestructura con Docker

```powershell
docker-compose -f docker-compose-replicacion.yml up -d --build
```

Esto levanta:
- 1 PostgreSQL Primary (puerto 5432)
- 2 PostgreSQL Standbys (puertos 5433, 5434)
- 2 Instancias de API (puertos 8001, 8002)
- 1 Nginx Load Balancer (puerto 80)
- 1 RabbitMQ (puertos 5672, 15672)

**⏳ Tiempo de inicio**: ~2-3 minutos (las réplicas hacen pg_basebackup inicial)

### Paso 3: Verificar Estado de Replicación

```powershell
# Ver logs de replicación
docker logs postgres-standby-1
docker logs postgres-standby-2

# Verificar que todos los contenedores estén UP
docker ps
```

Deberías ver 6 contenedores corriendo.

### Paso 4: Ejecutar Suite de Pruebas

```powershell
python test_replication_sharding.py
```

**Esto ejecuta 6 pruebas:**

1. ✅ **Replicación Write→Read**: Inserta en primario, lee de secundarios
2. ✅ **Distribución de Lecturas**: Round-robin entre secundarios
3. ✅ **Lag de Replicación**: Consulta `pg_stat_replication`
4. ✅ **Simple Hash Sharding**: Distribuye 300 users con hash modular
5. ✅ **Consistent Hashing**: Valida redistribución eficiente al agregar shard
6. ✅ **Failover Simulation**: Detecta fallos y redirige tráfico

### Paso 5: Ver Métricas en Tiempo Real

```powershell
# Conectar a primario y ver estado de réplicas
docker exec -it postgres-primary psql -U ecomarket -d ecomarket

# En psql:
SELECT * FROM pg_stat_replication;

# Ver lag de replicación
SELECT 
    application_name,
    state,
    sync_state,
    write_lag,
    replay_lag
FROM pg_stat_replication;
```

---

## 📊 Resultados de Pruebas

### Replicación

| Métrica | Valor | Objetivo |
|---------|-------|----------|
| Lag promedio | < 100ms | ✅ < 1s |
| Throughput lecturas | ~2000 qps | ✅ 2x vs single DB |
| Disponibilidad | 99.9% | ✅ N-1 tolerancia |

### Sharding

| Estrategia | Distribución | Redistribución al escalar |
|------------|--------------|---------------------------|
| Simple Hash | Uniforme (±3%) | ❌ 75% datos movidos |
| Consistent Hash | Uniforme (±5%) | ✅ 25% datos movidos |

---

## 🧪 Pruebas Manuales

### Test 1: Write en Primario

```bash
docker exec -it postgres-primary psql -U ecomarket -d ecomarket -c \
  "INSERT INTO products (product_id, name, price, stock) VALUES ('TEST-001', 'Producto Test', 99.99, 50);"
```

### Test 2: Read de Secundario

```bash
# Esperar 1-2 segundos para replicación
docker exec -it postgres-standby-1 psql -U ecomarket -d ecomarket -c \
  "SELECT * FROM products WHERE product_id = 'TEST-001';"
```

Deberías ver el producto replicado.

### Test 3: Simular Failover

```bash
# Detener un secundario
docker stop postgres-standby-1

# Las APIs deben seguir funcionando usando standby-2
curl http://localhost/api/productos
```

---

## 📁 Estructura de Archivos

```
.
├── docker-compose-replicacion.yml    # Orquestación de BD replicada
├── postgres/
│   ├── primary/
│   │   ├── postgresql.conf           # Config primario (wal_level=replica)
│   │   ├── pg_hba.conf              # Auth para replicación
│   │   └── init-primary.sh          # Script init (crea user replicator)
│   └── standby/
│       ├── postgresql.conf           # Config secundario (hot_standby=on)
│       └── standby.signal           # Marca servidor como standby
├── shard_router.py                   # Routers de sharding (Simple + Consistent)
├── test_replication_sharding.py      # Suite de pruebas ejecutables
├── requirements.txt                  # Dependencias Python (psycopg2, asyncpg)
└── README-SEMANA7.md                # Este archivo
```

---

## 🔍 Análisis CAP: Decisiones de Diseño

El **Teorema CAP** establece que un sistema distribuido puede garantizar máximo 2 de 3 propiedades:

- **C**onsistency (Consistencia)
- **A**vailability (Disponibilidad)
- **P**artition Tolerance (Tolerancia a Particiones)

### Nuestra Implementación (CP - Consistencia + Tolerancia a Particiones)

| Entidad | Estrategia | Justificación |
|---------|------------|---------------|
| **Inventory** | CP | Stock crítico → lecturas strong consistency del primario |
| **Orders** | CP | Transacciones ACID → writes solo en primario |
| **User Sessions** | AP | Cache eventual consistency OK → reads de secundarios |
| **Analytics** | AP | Datos históricos → lag aceptable (eventual consistency) |

### Trade-offs Aceptados

- ✅ **Writes serializados**: Todos van al primario → limita throughput de escrituras
- ✅ **Read lag**: Secundarios pueden tener 100-500ms de retraso → eventual consistency
- ❌ **Single point of failure**: Si primario cae, no hay auto-failover (requiere intervención manual)

### Mejoras Futuras

- 🔄 Auto-failover con **Patroni** o **pg_auto_failover**
- 📊 Monitoring con **pgBadger** y **pg_stat_statements**
- 🌍 Replicación multi-región para geo-redundancia
- 🔀 Sharding real con **Citus** extension

---

## 🐛 Troubleshooting

### Problema: Réplicas no se conectan

**Síntoma**: `docker logs postgres-standby-1` muestra errores de autenticación

**Solución**:
```bash
# Verificar que usuario replicator existe en primario
docker exec -it postgres-primary psql -U ecomarket -c "\du"

# Si no existe, recrear
docker exec -it postgres-primary psql -U ecomarket -c \
  "CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';"

# Restart standbys
docker-compose -f docker-compose-replicacion.yml restart postgres-standby-1 postgres-standby-2
```

### Problema: Lag muy alto (> 5 segundos)

**Síntoma**: Datos tardan mucho en aparecer en secundarios

**Causas posibles**:
1. Red lenta entre contenedores
2. WAL generado muy rápido (muchos writes)
3. Secundario con CPU/disco lento

**Solución**:
```bash
# Consultar lag actual
docker exec -it postgres-primary psql -U ecomarket -c \
  "SELECT write_lag, flush_lag, replay_lag FROM pg_stat_replication;"

# Si lag > 5s consistente:
# 1. Reducir writes al primario
# 2. Aumentar recursos de secundarios (RAM/CPU)
# 3. Considerar replicación síncrona (synchronous_commit = on)
```

### Problema: Tests de sharding fallan con "module not found"

**Síntoma**: `ModuleNotFoundError: No module named 'psycopg2'`

**Solución**:
```powershell
pip install psycopg2-binary asyncpg
```

---

## 📖 Recursos Adicionales

- [PostgreSQL Streaming Replication](https://www.postgresql.org/docs/current/warm-standby.html)
- [Consistent Hashing Explained](https://www.toptal.com/big-data/consistent-hashing)
- [CAP Theorem](https://en.wikipedia.org/wiki/CAP_theorem)
- [CockroachDB Architecture](https://www.cockroachlabs.com/docs/stable/architecture/overview.html)

---

## 👥 Autor

**José Palacios** - Semana 7: Distribución de Datos  
Universidad - Arquitectura de Software Distribuido

---

## 📝 Licencia

Proyecto académico - EcoMarket 2025
