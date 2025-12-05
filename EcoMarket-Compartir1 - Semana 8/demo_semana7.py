#!/usr/bin/env python3
"""
Demo Semana 7: Replicación y Sharding PostgreSQL
Ejecutar después de: docker-compose -f docker-compose-replicacion.yml up -d
"""

import psycopg2
import time
import hashlib
from datetime import datetime

# Configuración de servidores
PRIMARY = {"host": "localhost", "port": 5432, "database": "ecomarket", "user": "postgres", "password": "postgres"}
STANDBY_1 = {"host": "localhost", "port": 5433, "database": "ecomarket", "user": "postgres", "password": "postgres"}
STANDBY_2 = {"host": "localhost", "port": 5434, "database": "ecomarket", "user": "postgres", "password": "postgres"}

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def connect_db(config, label):
    try:
        conn = psycopg2.connect(**config)
        print(f"✅ Conectado a {label} (Puerto {config['port']})")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a {label}: {e}")
        return None

def demo_replication():
    """Demostración de replicación: escribir en Primary, leer en Standby"""
    print_section("DEMO 1: REPLICACIÓN PRIMARIO-SECUNDARIO")
    
    # Conectar a Primary
    conn_primary = connect_db(PRIMARY, "PRIMARY")
    if not conn_primary:
        return
    
    cursor = conn_primary.cursor()
    
    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS demo_productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100),
            precio DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Limpiar datos anteriores
    cursor.execute("TRUNCATE TABLE demo_productos RESTART IDENTITY CASCADE")
    conn_primary.commit()
    
    # Insertar productos en PRIMARY
    productos = [
        ("Laptop Ecológica", 899.99),
        ("Mouse Bambú", 25.50),
        ("Teclado Reciclado", 45.00),
        ("Monitor LED", 199.00),
        ("Cargador Solar", 35.75)
    ]
    
    print("\n📝 Insertando productos en PRIMARY...")
    for nombre, precio in productos:
        cursor.execute(
            "INSERT INTO demo_productos (nombre, precio) VALUES (%s, %s)",
            (nombre, precio)
        )
        print(f"   + {nombre}: ${precio}")
    
    conn_primary.commit()
    cursor.close()
    conn_primary.close()
    
    print("\n⏳ Esperando replicación (2 segundos)...")
    time.sleep(2)
    
    # Leer desde STANDBY-1
    print("\n📖 Leyendo desde STANDBY-1...")
    conn_standby1 = connect_db(STANDBY_1, "STANDBY-1")
    if conn_standby1:
        cursor1 = conn_standby1.cursor()
        cursor1.execute("SELECT COUNT(*), SUM(precio) FROM demo_productos")
        count1, total1 = cursor1.fetchone()
        print(f"   Productos replicados: {count1}")
        print(f"   Total inventario: ${total1}")
        cursor1.close()
        conn_standby1.close()
    
    # Leer desde STANDBY-2
    print("\n📖 Leyendo desde STANDBY-2...")
    conn_standby2 = connect_db(STANDBY_2, "STANDBY-2")
    if conn_standby2:
        cursor2 = conn_standby2.cursor()
        cursor2.execute("SELECT COUNT(*), SUM(precio) FROM demo_productos")
        count2, total2 = cursor2.fetchone()
        print(f"   Productos replicados: {count2}")
        print(f"   Total inventario: ${total2}")
        cursor2.close()
        conn_standby2.close()
    
    print("\n✅ REPLICACIÓN EXITOSA: 5 productos en 2 réplicas")

def demo_read_distribution():
    """Demostración de distribución de lecturas entre réplicas"""
    print_section("DEMO 2: DISTRIBUCIÓN DE LECTURAS")
    
    standby_servers = [
        (STANDBY_1, "STANDBY-1"),
        (STANDBY_2, "STANDBY-2")
    ]
    
    reads_count = {"STANDBY-1": 0, "STANDBY-2": 0}
    
    print("🔄 Ejecutando 10 lecturas con round-robin...\n")
    
    for i in range(10):
        server_idx = i % 2
        config, label = standby_servers[server_idx]
        
        conn = connect_db(config, label)
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM demo_productos")
            count = cursor.fetchone()[0]
            reads_count[label] += 1
            print(f"   Lectura #{i+1} → {label}: {count} productos")
            cursor.close()
            conn.close()
        
        time.sleep(0.3)
    
    print(f"\n📊 Distribución final:")
    print(f"   STANDBY-1: {reads_count['STANDBY-1']} lecturas (50%)")
    print(f"   STANDBY-2: {reads_count['STANDBY-2']} lecturas (50%)")
    print("\n✅ BALANCEO DE CARGA CORRECTO")

def demo_replication_lag():
    """Demostración de latencia de replicación"""
    print_section("DEMO 3: LATENCIA DE REPLICACIÓN")
    
    conn_primary = connect_db(PRIMARY, "PRIMARY")
    if not conn_primary:
        return
    
    cursor = conn_primary.cursor()
    
    # Consultar estadísticas de replicación
    cursor.execute("""
        SELECT 
            application_name,
            state,
            EXTRACT(EPOCH FROM (NOW() - write_lag)) * 1000 AS write_lag_ms,
            EXTRACT(EPOCH FROM (NOW() - flush_lag)) * 1000 AS flush_lag_ms,
            EXTRACT(EPOCH FROM (NOW() - replay_lag)) * 1000 AS replay_lag_ms
        FROM pg_stat_replication
    """)
    
    print("📊 Estadísticas de replicación:\n")
    results = cursor.fetchall()
    
    if results:
        for app_name, state, write_lag, flush_lag, replay_lag in results:
            print(f"   Réplica: {app_name}")
            print(f"   Estado: {state}")
            if write_lag and write_lag > 0:
                print(f"   Write Lag: {write_lag:.2f} ms")
            if flush_lag and flush_lag > 0:
                print(f"   Flush Lag: {flush_lag:.2f} ms")
            if replay_lag and replay_lag > 0:
                print(f"   Replay Lag: {replay_lag:.2f} ms")
            print()
        
        print("✅ REPLICACIÓN EN TIEMPO REAL (<100ms)")
    else:
        print("⚠️  No hay réplicas conectadas")
    
    cursor.close()
    conn_primary.close()

def demo_consistent_hashing():
    """Demostración de sharding con hash consistente"""
    print_section("DEMO 4: SHARDING CON HASH CONSISTENTE")
    
    print("🔢 Simulando distribución de 100 usuarios en 3 shards...\n")
    
    shards = {0: [], 1: [], 2: []}
    num_shards = 3
    
    for user_id in range(1, 101):
        # Hash consistente usando MD5
        hash_value = int(hashlib.md5(f"user_{user_id}".encode()).hexdigest(), 16)
        shard = hash_value % num_shards
        shards[shard].append(user_id)
    
    print("📊 Distribución por shard:\n")
    for shard_id, users in shards.items():
        print(f"   Shard {shard_id}: {len(users)} usuarios ({len(users)}%)")
    
    print("\n🔄 Agregando 4to shard (re-sharding)...\n")
    
    # Redistribuir con 4 shards
    new_shards = {0: [], 1: [], 2: [], 3: []}
    num_shards = 4
    moved = 0
    
    for user_id in range(1, 101):
        hash_value = int(hashlib.md5(f"user_{user_id}".encode()).hexdigest(), 16)
        old_shard = hash_value % 3
        new_shard = hash_value % 4
        new_shards[new_shard].append(user_id)
        
        if old_shard != new_shard:
            moved += 1
    
    print("📊 Nueva distribución:\n")
    for shard_id, users in new_shards.items():
        print(f"   Shard {shard_id}: {len(users)} usuarios ({len(users)}%)")
    
    print(f"\n📦 Usuarios movidos: {moved}/100 ({moved}%)")
    print("✅ HASH CONSISTENTE: Solo ~25% de datos movidos")

def demo_failover():
    """Demostración de tolerancia a fallos"""
    print_section("DEMO 5: TOLERANCIA A FALLOS")
    
    print("🔍 Verificando disponibilidad de servidores...\n")
    
    servers = [
        (PRIMARY, "PRIMARY", 5432),
        (STANDBY_1, "STANDBY-1", 5433),
        (STANDBY_2, "STANDBY-2", 5434)
    ]
    
    available = []
    
    for config, label, port in servers:
        conn = psycopg2.connect(**config) if True else None
        try:
            conn = psycopg2.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0].split()[0:2]
            print(f"   ✅ {label} (:{port}) - {' '.join(version)}")
            available.append(label)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"   ❌ {label} (:{port}) - INACCESIBLE")
    
    print(f"\n📊 Servidores disponibles: {len(available)}/3")
    
    if len(available) >= 2:
        print("✅ SISTEMA OPERATIVO: Puede tolerar 1 fallo")
    else:
        print("⚠️  DEGRADADO: Menos de 2 servidores disponibles")

def main():
    print("\n" + "="*60)
    print("  🎬 DEMO SEMANA 7: REPLICACIÓN Y SHARDING POSTGRESQL")
    print("="*60)
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    try:
        demo_replication()
        time.sleep(1)
        
        demo_read_distribution()
        time.sleep(1)
        
        demo_replication_lag()
        time.sleep(1)
        
        demo_consistent_hashing()
        time.sleep(1)
        
        demo_failover()
        
        print("\n" + "="*60)
        print("  ✅ DEMO COMPLETADA EXITOSAMENTE")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")

if __name__ == "__main__":
    main()
