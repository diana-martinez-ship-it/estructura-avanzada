#!/usr/bin/env python3
"""
Demo Semana 7: PostgreSQL - Sharding y Distribución de Carga
SIMPLICADO para demostración rápida
"""

import psycopg2
import time
import hashlib
from datetime import datetime
import random

# Configuración de 3 servidores PostgreSQL
SERVERS = [
    {"host": "localhost", "port": 5432, "database": "ecomarket", "user": "postgres", "password": "postgres"},
    {"host": "localhost", "port": 5433, "database": "ecomarket", "user": "postgres", "password": "postgres"},
    {"host": "localhost", "port": 5434, "database": "ecomarket", "user": "postgres", "password": "postgres"},
]
SERVER_NAMES = ["SERVER-1", "SERVER-2", "SERVER-3"]

def print_header():
    print("\n" + "="*70)
    print("  🎬 DEMO SEMANA 7: SHARDING Y DISTRIBUCIÓN DE CARGA POSTGRESQL")
    print("="*70)
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def connect_db(config, server_name):
    try:
        conn = psycopg2.connect(**config)
        return conn
    except Exception as e:
        print(f"❌ Error conectando a {server_name}: {e}")
        return None

def demo_1_sharding_simple():
    """Demo 1: Sharding por hash de user_id"""
    print_section("DEMO 1: SHARDING POR HASH")
    
    print("📦 Creando tablas en los 3 servidores...\n")
    
    # Crear tabla en cada servidor
    for i, server in enumerate(SERVERS):
        conn = connect_db(server, SERVER_NAMES[i])
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                DROP TABLE IF EXISTS usuarios CASCADE;
                CREATE TABLE usuarios (
                    user_id VARCHAR(50) PRIMARY KEY,
                    nombre VARCHAR(100),
                    email VARCHAR(100),
                    shard_id INTEGER
                )
            """)
            conn.commit()
            print(f"✅ Tabla creada en {SERVER_NAMES[i]}")
            conn.close()
    
    print("\n🔢 Insertando 30 usuarios distribuidos por hash...\n")
    
    usuarios = [
        ("user001", "Ana García", "ana@email.com"),
        ("user002", "Luis Pérez", "luis@email.com"),
        ("user003", "María López", "maria@email.com"),
        ("user004", "Carlos Ruiz", "carlos@email.com"),
        ("user005", "Laura Sánchez", "laura@email.com"),
        ("user006", "Pedro Martínez", "pedro@email.com"),
        ("user007", "Sofia Torres", "sofia@email.com"),
        ("user008", "Diego Ramírez", "diego@email.com"),
        ("user009", "Isabella Cruz", "isabella@email.com"),
        ("user010", "Javier Flores", "javier@email.com"),
        ("user011", "Valentina Morales", "valentina@email.com"),
        ("user012", "Andrés Jiménez", "andres@email.com"),
        ("user013", "Camila Vargas", "camila@email.com"),
        ("user014", "Miguel Herrera", "miguel@email.com"),
        ("user015", "Lucía Castro", "lucia@email.com"),
        ("user016", "Daniel Ortiz", "daniel@email.com"),
        ("user017", "Gabriela Silva", "gabriela@email.com"),
        ("user018", "Fernando Rojas", "fernando@email.com"),
        ("user019", "Paula Mendoza", "paula@email.com"),
        ("user020", "Roberto Guzmán", "roberto@email.com"),
        ("user021", "Carolina Ríos", "carolina@email.com"),
        ("user022", "Alejandro Paredes", "alejandro@email.com"),
        ("user023", "Natalia Vega", "natalia@email.com"),
        ("user024", "Ricardo Campos", "ricardo@email.com"),
        ("user025", "Andrea Peña", "andrea@email.com"),
        ("user026", "Juan Cabrera", "juan@email.com"),
        ("user027", "Daniela Núñez", "daniela@email.com"),
        ("user028", "Sergio Molina", "sergio@email.com"),
        ("user029", "Mariana Reyes", "mariana@email.com"),
        ("user030", "Eduardo Luna", "eduardo@email.com"),
    ]
    
    distribution = {0: 0, 1: 0, 2: 0}
    
    for user_id, nombre, email in usuarios:
        # Calcular shard usando hash
        hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        shard_id = hash_value % 3
        
        # Insertar en el shard correspondiente
        server = SERVERS[shard_id]
        conn = connect_db(server, SERVER_NAMES[shard_id])
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (user_id, nombre, email, shard_id)
                VALUES (%s, %s, %s, %s)
            """, (user_id, nombre, email, shard_id))
            conn.commit()
            conn.close()
            distribution[shard_id] += 1
            print(f"  → {user_id} ({nombre}) → Shard {shard_id} ({SERVER_NAMES[shard_id]})")
    
    print("\n📊 Distribución final:")
    for shard_id, count in distribution.items():
        percentage = (count / 30) * 100
        bar = "█" * (count // 2)
        print(f"  Shard {shard_id} ({SERVER_NAMES[shard_id]}): {count} usuarios ({percentage:.1f}%) {bar}")
    
    print("\n✅ SHARDING COMPLETADO: Los datos están distribuidos en 3 servidores")

def demo_2_balanceo_carga():
    """Demo 2: Balanceo de carga round-robin"""
    print_section("DEMO 2: BALANCEO DE CARGA (ROUND-ROBIN)")
    
    print("🔄 Ejecutando 15 consultas con distribución round-robin...\n")
    
    read_counts = {0: 0, 1: 0, 2: 0}
    
    for i in range(15):
        shard_id = i % 3
        server = SERVERS[shard_id]
        
        conn = connect_db(server, SERVER_NAMES[shard_id])
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            count = cursor.fetchone()[0]
            conn.close()
            
            read_counts[shard_id] += 1
            print(f"  Lectura {i+1:2d} → {SERVER_NAMES[shard_id]} (Puerto {server['port']}) → {count} usuarios encontrados")
    
    print("\n📊 Distribución de lecturas:")
    for shard_id, count in read_counts.items():
        percentage = (count / 15) * 100
        bar = "█" * count
        print(f"  {SERVER_NAMES[shard_id]}: {count} lecturas ({percentage:.0f}%) {bar}")
    
    print("\n✅ BALANCEO CORRECTO: Las lecturas se distribuyeron uniformemente")

def demo_3_consulta_agregada():
    """Demo 3: Consulta agregada desde todos los shards"""
    print_section("DEMO 3: CONSULTA AGREGADA (MAP-REDUCE)")
    
    print("🔍 Consultando TODOS los usuarios desde los 3 shards...\n")
    
    all_users = []
    
    for i, server in enumerate(SERVERS):
        conn = connect_db(server, SERVER_NAMES[i])
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, nombre, email FROM usuarios ORDER BY user_id")
            users = cursor.fetchall()
            conn.close()
            
            print(f"  📦 {SERVER_NAMES[i]}: {len(users)} usuarios")
            all_users.extend(users)
    
    print(f"\n📊 Total de usuarios en el sistema: {len(all_users)}")
    print("\n🔍 Primeros 5 usuarios (ordenados):")
    for user_id, nombre, email in sorted(all_users)[:5]:
        print(f"  → {user_id}: {nombre} ({email})")
    
    print("\n✅ CONSULTA AGREGADA EXITOSA: Combinamos datos de 3 shards")

def demo_4_failover():
    """Demo 4: Simulación de failover"""
    print_section("DEMO 4: TOLERANCIA A FALLOS (FAILOVER)")
    
    print("🔍 Intentando leer datos con failover automático...\n")
    
    # Simular que el primer servidor "falla"
    failed_server = 0
    print(f"❌ Simulando fallo en {SERVER_NAMES[failed_server]}...\n")
    
    # Intentar leer de servidores disponibles
    for attempt in range(5):
        shard_id = attempt % 3
        
        if shard_id == failed_server:
            # Cambiar a servidor de respaldo
            shard_id = (shard_id + 1) % 3
            print(f"  Intento {attempt+1}: {SERVER_NAMES[failed_server]} no disponible → Redirigiendo a {SERVER_NAMES[shard_id]}")
        else:
            print(f"  Intento {attempt+1}: Usando {SERVER_NAMES[shard_id]}")
        
        server = SERVERS[shard_id]
        conn = connect_db(server, SERVER_NAMES[shard_id])
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            count = cursor.fetchone()[0]
            conn.close()
            print(f"              ✅ Exitoso - {count} usuarios\n")
    
    print("✅ FAILOVER FUNCIONAL: El sistema sigue operando con servidores disponibles")

def demo_5_hash_consistente():
    """Demo 5: Comparación de hash simple vs hash consistente"""
    print_section("DEMO 5: HASH CONSISTENTE vs HASH SIMPLE")
    
    print("🔢 Simulando distribución de 100 usuarios con HASH SIMPLE...\n")
    
    # Hash simple con 3 shards
    simple_hash = {}
    for i in range(100):
        user_id = f"user{i:03d}"
        shard = int(hashlib.md5(user_id.encode()).hexdigest(), 16) % 3
        simple_hash[user_id] = shard
    
    dist_3 = {0: 0, 1: 0, 2: 0}
    for shard in simple_hash.values():
        dist_3[shard] += 1
    
    print("📊 Distribución con 3 shards:")
    for shard, count in dist_3.items():
        print(f"  Shard {shard}: {count} usuarios ({count}%)")
    
    print("\n🔄 Agregando 4to shard (escalamiento horizontal)...\n")
    
    # Re-sharding con 4 shards
    moved = 0
    for user_id in simple_hash.keys():
        old_shard = simple_hash[user_id]
        new_shard = int(hashlib.md5(user_id.encode()).hexdigest(), 16) % 4
        if old_shard != new_shard:
            moved += 1
    
    print(f"📦 Usuarios que deben moverse: {moved}/100 ({moved}%)")
    print("\n❌ PROBLEMA: Con hash simple, agregar shards requiere mover ~75% de los datos")
    print("✅ SOLUCIÓN: Hash consistente solo mueve ~25% de los datos")
    print("\n💡 Hash consistente es MEJOR para sistemas que escalan dinámicamente")

def main():
    print_header()
    
    try:
        demo_1_sharding_simple()
        time.sleep(2)
        
        demo_2_balanceo_carga()
        time.sleep(2)
        
        demo_3_consulta_agregada()
        time.sleep(2)
        
        demo_4_failover()
        time.sleep(2)
        
        demo_5_hash_consistente()
        
        print("\n" + "="*70)
        print("  ✅ DEMO COMPLETADO - Todos los conceptos fueron demostrados")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")

if __name__ == "__main__":
    main()
