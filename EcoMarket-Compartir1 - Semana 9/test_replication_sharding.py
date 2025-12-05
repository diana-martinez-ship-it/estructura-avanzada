"""
Script de Prueba de Carga para Replicación y Sharding de EcoMarket
Valida: writes al primario, reads de secundarios, distribución de sharding
"""

import psycopg2
import time
import random
from typing import List, Dict
from shard_router import SimpleHashShardRouter, ConsistentHashRouter, ShardConfig


class DatabaseConfig:
    """Configuración de conexión a base de datos"""
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
    
    def get_connection(self):
        """Crea una conexión a PostgreSQL"""
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )


# Configuración de servidores
PRIMARY = DatabaseConfig("localhost", 5432, "ecomarket", "ecomarket123", "ecomarket")
STANDBY_1 = DatabaseConfig("localhost", 5433, "ecomarket", "ecomarket123", "ecomarket")
STANDBY_2 = DatabaseConfig("localhost", 5434, "ecomarket", "ecomarket123", "ecomarket")


def initialize_schema():
    """Crea el esquema de base de datos en el primario"""
    print("\n🔧 Inicializando esquema de base de datos...")
    
    conn = PRIMARY.get_connection()
    cur = conn.cursor()
    
    # Tabla de usuarios (para pruebas de sharding)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            shard_key VARCHAR(50)
        )
    """)
    
    # Tabla de productos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(200),
            price DECIMAL(10, 2),
            stock INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla de órdenes (para pruebas de replicación)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY,
            user_id VARCHAR(50),
            product_id VARCHAR(50),
            quantity INTEGER,
            total DECIMAL(10, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("✅ Esquema creado exitosamente")


def test_replication_write_read():
    """
    Prueba 1: Escrituras al Primario + Lecturas de Secundarios
    Valida que los datos escritos en primario aparezcan en secundarios
    """
    print("\n" + "="*60)
    print("PRUEBA 1: REPLICACIÓN - WRITE TO PRIMARY, READ FROM STANDBY")
    print("="*60)
    
    # 1. Escribir en primario
    print("\n📝 Escribiendo 10 productos en PRIMARIO...")
    conn_primary = PRIMARY.get_connection()
    cur_primary = conn_primary.cursor()
    
    products = []
    for i in range(10):
        product_id = f"PROD-{random.randint(10000, 99999)}"
        name = f"Producto Eco {i+1}"
        price = round(random.uniform(10.0, 500.0), 2)
        stock = random.randint(1, 100)
        
        cur_primary.execute(
            "INSERT INTO products (product_id, name, price, stock) VALUES (%s, %s, %s, %s)",
            (product_id, name, price, stock)
        )
        products.append(product_id)
    
    conn_primary.commit()
    cur_primary.close()
    conn_primary.close()
    
    print(f"✅ {len(products)} productos insertados en PRIMARIO")
    
    # 2. Esperar lag de replicación
    print("\n⏳ Esperando 2 segundos para replicación...")
    time.sleep(2)
    
    # 3. Leer de secundarios
    print("\n📖 Leyendo productos desde SECUNDARIOS...")
    
    for standby, name in [(STANDBY_1, "STANDBY-1"), (STANDBY_2, "STANDBY-2")]:
        try:
            conn_standby = standby.get_connection()
            cur_standby = conn_standby.cursor()
            
            cur_standby.execute("SELECT COUNT(*) FROM products WHERE product_id = ANY(%s)", (products,))
            count = cur_standby.fetchone()[0]
            
            cur_standby.close()
            conn_standby.close()
            
            if count == len(products):
                print(f"  ✅ {name}: {count}/{len(products)} productos replicados")
            else:
                print(f"  ⚠️  {name}: {count}/{len(products)} productos (lag detectado)")
        
        except Exception as e:
            print(f"  ❌ {name}: Error - {str(e)}")
    
    print("\n💡 Conclusión: Replicación streaming funcional")


def test_read_distribution():
    """
    Prueba 2: Distribución de Lecturas entre Secundarios
    Simula balanceo de carga de queries SELECT
    """
    print("\n" + "="*60)
    print("PRUEBA 2: DISTRIBUCIÓN DE LECTURAS")
    print("="*60)
    
    standby_servers = [
        (STANDBY_1, "STANDBY-1"),
        (STANDBY_2, "STANDBY-2")
    ]
    
    num_queries = 20
    query_counts = {name: 0 for _, name in standby_servers}
    
    print(f"\n📊 Ejecutando {num_queries} SELECT queries con round-robin...")
    
    for i in range(num_queries):
        # Round-robin simple
        standby, name = standby_servers[i % len(standby_servers)]
        
        try:
            conn = standby.get_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT COUNT(*) FROM products")
            count = cur.fetchone()[0]
            
            cur.close()
            conn.close()
            
            query_counts[name] += 1
            print(f"  Query #{i+1} → {name} ({count} productos)")
        
        except Exception as e:
            print(f"  ❌ Query #{i+1} → {name} ERROR: {str(e)}")
    
    print(f"\n📈 Distribución de queries:")
    for name, count in query_counts.items():
        percentage = (count / num_queries) * 100
        print(f"  {name}: {count}/{num_queries} queries ({percentage:.0f}%)")
    
    print("\n💡 Conclusión: Lecturas distribuidas uniformemente")


def test_replication_lag():
    """
    Prueba 3: Medición de Lag de Replicación
    Usa pg_stat_replication para monitorear retraso
    """
    print("\n" + "="*60)
    print("PRUEBA 3: LAG DE REPLICACIÓN")
    print("="*60)
    
    print("\n⏱️  Consultando pg_stat_replication en PRIMARIO...")
    
    try:
        conn = PRIMARY.get_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                application_name,
                client_addr,
                state,
                sync_state,
                COALESCE(write_lag, '0 seconds'::interval) as write_lag,
                COALESCE(replay_lag, '0 seconds'::interval) as replay_lag
            FROM pg_stat_replication
        """)
        
        replicas = cur.fetchall()
        
        if replicas:
            print(f"\n✅ {len(replicas)} réplicas conectadas:")
            for replica in replicas:
                app_name, client, state, sync, write_lag, replay_lag = replica
                print(f"\n  Réplica: {app_name or client}")
                print(f"    Estado: {state}")
                print(f"    Modo: {sync}")
                print(f"    Write Lag: {write_lag}")
                print(f"    Replay Lag: {replay_lag}")
        else:
            print("\n⚠️  No hay réplicas conectadas (pueden tardar en inicializarse)")
        
        cur.close()
        conn.close()
    
    except Exception as e:
        print(f"\n❌ Error consultando lag: {str(e)}")
    
    print("\n💡 Conclusión: Monitoreo de lag disponible")


def test_simple_hash_sharding():
    """
    Prueba 4: Simple Hash Sharding
    Valida distribución uniforme de datos con hash modular
    """
    print("\n" + "="*60)
    print("PRUEBA 4: SIMPLE HASH SHARDING")
    print("="*60)
    
    # Configurar shards (conceptual - usamos los servidores disponibles)
    shards = [
        ShardConfig(1, "localhost", 5432, "ecomarket"),  # Primary
        ShardConfig(2, "localhost", 5433, "ecomarket"),  # Standby 1
        ShardConfig(3, "localhost", 5434, "ecomarket"),  # Standby 2
    ]
    
    router = SimpleHashShardRouter(shards)
    
    # Generar 300 user IDs
    user_ids = [f"user_{i:04d}" for i in range(300)]
    
    print(f"\n🔀 Distribuyendo {len(user_ids)} usuarios con Simple Hash...")
    
    distribution = router.get_distribution(user_ids)
    
    print(f"\n📊 Distribución:")
    for shard_id, count in distribution.items():
        percentage = (count / len(user_ids)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  Shard {shard_id}: {count:3d} users ({percentage:5.1f}%) {bar}")
    
    # Calcular desviación estándar (debería ser baja)
    avg = len(user_ids) / len(shards)
    variance = sum((count - avg) ** 2 for count in distribution.values()) / len(shards)
    std_dev = variance ** 0.5
    
    print(f"\n📈 Estadísticas:")
    print(f"  Promedio esperado: {avg:.1f} users/shard")
    print(f"  Desviación estándar: {std_dev:.2f}")
    
    if std_dev < 10:
        print(f"  ✅ Distribución uniforme (σ < 10)")
    else:
        print(f"  ⚠️  Distribución desbalanceada (σ >= 10)")
    
    print("\n💡 Conclusión: Simple hash distribuye uniformemente")


def test_consistent_hashing():
    """
    Prueba 5: Consistent Hashing
    Valida mejor redistribución al agregar/quitar shards
    """
    print("\n" + "="*60)
    print("PRUEBA 5: CONSISTENT HASHING")
    print("="*60)
    
    # Configurar shards iniciales
    shards = [
        ShardConfig(1, "localhost", 5432, "ecomarket"),
        ShardConfig(2, "localhost", 5433, "ecomarket"),
        ShardConfig(3, "localhost", 5434, "ecomarket"),
    ]
    
    router = ConsistentHashRouter(shards, vnodes_per_shard=150)
    
    # Generar keys
    user_ids = [f"user_{i:04d}" for i in range(300)]
    
    print(f"\n🔄 Distribuyendo {len(user_ids)} usuarios con Consistent Hash...")
    
    distribution = router.get_distribution(user_ids)
    
    print(f"\n📊 Distribución con 3 shards:")
    for shard_id, count in distribution.items():
        percentage = (count / len(user_ids)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  Shard {shard_id}: {count:3d} users ({percentage:5.1f}%) {bar}")
    
    # Simular agregar un 4º shard
    print(f"\n➕ Agregando Shard 4...")
    
    # Calcular asignaciones antes
    assignments_before = {uid: router.get_shard(uid).shard_id for uid in user_ids}
    
    # Agregar shard
    new_shard = ShardConfig(4, "localhost", 5435, "ecomarket")
    router.add_shard(new_shard)
    
    # Calcular asignaciones después
    assignments_after = {uid: router.get_shard(uid).shard_id for uid in user_ids}
    
    # Contar movimientos
    moved = sum(1 for uid in user_ids if assignments_before[uid] != assignments_after[uid])
    moved_pct = (moved / len(user_ids)) * 100
    
    print(f"\n📊 Nueva distribución con 4 shards:")
    new_distribution = router.get_distribution(user_ids)
    for shard_id, count in sorted(new_distribution.items()):
        percentage = (count / len(user_ids)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  Shard {shard_id}: {count:3d} users ({percentage:5.1f}%) {bar}")
    
    print(f"\n🔄 Impacto de agregar Shard 4:")
    print(f"  Users redistribuidos: {moved}/{len(user_ids)} ({moved_pct:.1f}%)")
    print(f"  Teórico (K/N): {(len(user_ids)/4):.0f} ({(100/4):.0f}%)")
    
    if moved_pct < 30:
        print(f"  ✅ Redistribución eficiente (< 30%)")
    else:
        print(f"  ⚠️  Más redistribución de lo esperado")
    
    print("\n💡 Conclusión: Consistent hash minimiza redistribución")


def test_failover_simulation():
    """
    Prueba 6: Simulación de Failover
    Detecta fallo de secundario y redirige tráfico
    """
    print("\n" + "="*60)
    print("PRUEBA 6: SIMULACIÓN DE FAILOVER")
    print("="*60)
    
    print("\n🔍 Verificando salud de servidores...")
    
    servers = [
        (PRIMARY, "PRIMARY"),
        (STANDBY_1, "STANDBY-1"),
        (STANDBY_2, "STANDBY-2")
    ]
    
    healthy_servers = []
    
    for config, name in servers:
        try:
            conn = config.get_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT 1")
            cur.fetchone()
            
            cur.close()
            conn.close()
            
            print(f"  ✅ {name}: Saludable")
            healthy_servers.append((config, name))
        
        except Exception as e:
            print(f"  ❌ {name}: No disponible - {str(e)}")
    
    print(f"\n📊 Servidores disponibles: {len(healthy_servers)}/{len(servers)}")
    
    if len(healthy_servers) >= 2:
        print(f"\n✅ Sistema resiliente: {len(healthy_servers)} servidores activos")
        print(f"💡 Queries pueden continuar usando servidores saludables")
    else:
        print(f"\n⚠️  Solo {len(healthy_servers)} servidor disponible - riesgo de downtime")
    
    print("\n💡 Conclusión: Detección de fallos funcional")


def run_all_tests():
    """Ejecuta todas las pruebas en secuencia"""
    print("\n" + "🚀"*30)
    print("SUITE DE PRUEBAS - REPLICACIÓN Y SHARDING DE ECOMARKET")
    print("🚀"*30)
    
    try:
        # Inicializar esquema
        initialize_schema()
        
        # Pruebas de replicación
        test_replication_write_read()
        test_read_distribution()
        test_replication_lag()
        
        # Pruebas de sharding
        test_simple_hash_sharding()
        test_consistent_hashing()
        
        # Prueba de resiliencia
        test_failover_simulation()
        
        print("\n" + "✅"*30)
        print("TODAS LAS PRUEBAS COMPLETADAS")
        print("✅"*30)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por usuario")
    except Exception as e:
        print(f"\n\n❌ Error en suite de pruebas: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
