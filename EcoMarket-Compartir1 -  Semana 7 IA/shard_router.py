"""
Router de Sharding para EcoMarket
Implementa estrategias de particionamiento de datos:
1. Simple Hash Sharding
2. Consistent Hashing (para mejor redistribución)
"""

import hashlib
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class ShardConfig:
    """Configuración de un shard"""
    shard_id: int
    host: str
    port: int
    database: str


class SimpleHashShardRouter:
    """
    Router de sharding simple basado en hash modular
    Formula: shard_id = hash(key) % num_shards
    
    ⚠️ Problema: Al agregar/quitar shards, requiere redistribuir muchos datos
    """
    
    def __init__(self, shards: List[ShardConfig]):
        self.shards = shards
        self.num_shards = len(shards)
    
    def get_shard(self, key: str) -> ShardConfig:
        """
        Determina el shard para una key dada
        
        Args:
            key: Identificador único (ej: user_id, product_id)
        
        Returns:
            ShardConfig del shard asignado
        """
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        shard_index = hash_value % self.num_shards
        return self.shards[shard_index]
    
    def get_distribution(self, keys: List[str]) -> Dict[int, int]:
        """Analiza la distribución de keys entre shards"""
        distribution = {shard.shard_id: 0 for shard in self.shards}
        for key in keys:
            shard = self.get_shard(key)
            distribution[shard.shard_id] += 1
        return distribution


class ConsistentHashRouter:
    """
    Router con Consistent Hashing usando virtual nodes
    
    Ventajas:
    - Al agregar/quitar shards, solo mueve K/N datos (K=keys totales, N=num shards)
    - Distribución más uniforme con virtual nodes
    
    Algoritmo:
    1. Crea múltiples "virtual nodes" por cada shard físico
    2. Posiciona virtual nodes en un ring hash (0 a 2^32-1)
    3. Para cada key, encuentra el próximo virtual node en sentido horario
    """
    
    def __init__(self, shards: List[ShardConfig], vnodes_per_shard: int = 150):
        self.shards = {shard.shard_id: shard for shard in shards}
        self.vnodes_per_shard = vnodes_per_shard
        self.ring: Dict[int, int] = {}  # hash_value -> shard_id
        self._build_ring()
    
    def _hash(self, key: str) -> int:
        """Genera hash de 32 bits"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16) % (2**32)
    
    def _build_ring(self):
        """Construye el ring con virtual nodes"""
        for shard in self.shards.values():
            for vnode_id in range(self.vnodes_per_shard):
                # Crea virtual node único para cada shard
                vnode_key = f"{shard.host}:{shard.port}:vnode{vnode_id}"
                hash_value = self._hash(vnode_key)
                self.ring[hash_value] = shard.shard_id
        
        # Ordena el ring para búsqueda binaria eficiente
        self.sorted_keys = sorted(self.ring.keys())
    
    def get_shard(self, key: str) -> ShardConfig:
        """
        Encuentra el shard para una key usando consistent hashing
        
        Busca el primer virtual node >= hash(key) en el ring
        Si no encuentra, wraparound al primer nodo
        """
        if not self.ring:
            raise ValueError("No hay shards configurados")
        
        hash_value = self._hash(key)
        
        # Búsqueda binaria del próximo nodo
        for ring_key in self.sorted_keys:
            if ring_key >= hash_value:
                shard_id = self.ring[ring_key]
                return self.shards[shard_id]
        
        # Wraparound al primer nodo del ring
        shard_id = self.ring[self.sorted_keys[0]]
        return self.shards[shard_id]
    
    def add_shard(self, shard: ShardConfig):
        """Agrega un nuevo shard al ring"""
        self.shards[shard.shard_id] = shard
        for vnode_id in range(self.vnodes_per_shard):
            vnode_key = f"{shard.host}:{shard.port}:vnode{vnode_id}"
            hash_value = self._hash(vnode_key)
            self.ring[hash_value] = shard.shard_id
        self.sorted_keys = sorted(self.ring.keys())
    
    def remove_shard(self, shard_id: int):
        """Remueve un shard del ring"""
        if shard_id not in self.shards:
            return
        
        shard = self.shards[shard_id]
        # Remueve todos los virtual nodes de este shard
        keys_to_remove = []
        for hash_val, sid in self.ring.items():
            if sid == shard_id:
                keys_to_remove.append(hash_val)
        
        for key in keys_to_remove:
            del self.ring[key]
        
        del self.shards[shard_id]
        self.sorted_keys = sorted(self.ring.keys())
    
    def get_distribution(self, keys: List[str]) -> Dict[int, int]:
        """Analiza la distribución de keys entre shards"""
        distribution = {shard_id: 0 for shard_id in self.shards.keys()}
        for key in keys:
            shard = self.get_shard(key)
            distribution[shard.shard_id] += 1
        return distribution


# ===========================================
# Ejemplo de Uso y Comparación
# ===========================================

if __name__ == "__main__":
    # Configuración de shards (conceptual - usa secundarios para simulación)
    shards = [
        ShardConfig(shard_id=1, host="postgres-primary", port=5432, database="ecomarket"),
        ShardConfig(shard_id=2, host="postgres-standby-1", port=5432, database="ecomarket"),
        ShardConfig(shard_id=3, host="postgres-standby-2", port=5432, database="ecomarket"),
    ]
    
    # Generar keys de prueba (user IDs)
    test_keys = [f"user_{i}" for i in range(1000)]
    
    print("=" * 60)
    print("COMPARACIÓN: Simple Hash vs Consistent Hash")
    print("=" * 60)
    
    # 1. Simple Hash Router
    print("\n1️⃣  SIMPLE HASH ROUTER")
    print("-" * 60)
    simple_router = SimpleHashShardRouter(shards)
    simple_dist = simple_router.get_distribution(test_keys)
    
    print("Distribución con 3 shards:")
    for shard_id, count in simple_dist.items():
        percentage = (count / len(test_keys)) * 100
        print(f"  Shard {shard_id}: {count} keys ({percentage:.1f}%)")
    
    # Simular agregar un shard
    print("\n⚠️  Si agregamos un 4º shard:")
    shards_4 = shards + [ShardConfig(4, "new-host", 5432, "ecomarket")]
    simple_router_4 = SimpleHashShardRouter(shards_4)
    
    # Calcular cuántas keys cambiarían de shard
    moved_keys = 0
    for key in test_keys:
        old_shard = simple_router.get_shard(key).shard_id
        new_shard = simple_router_4.get_shard(key).shard_id
        if old_shard != new_shard:
            moved_keys += 1
    
    print(f"  Keys que cambiarían de shard: {moved_keys}/{len(test_keys)} ({(moved_keys/len(test_keys)*100):.1f}%)")
    print(f"  ❌ Requiere redistribuir ~75% de los datos!")
    
    # 2. Consistent Hash Router
    print("\n\n2️⃣  CONSISTENT HASH ROUTER")
    print("-" * 60)
    consistent_router = ConsistentHashRouter(shards, vnodes_per_shard=150)
    consistent_dist = consistent_router.get_distribution(test_keys)
    
    print("Distribución con 3 shards:")
    for shard_id, count in consistent_dist.items():
        percentage = (count / len(test_keys)) * 100
        print(f"  Shard {shard_id}: {count} keys ({percentage:.1f}%)")
    
    # Agregar un shard
    print("\n✅ Agregamos un 4º shard:")
    new_shard = ShardConfig(4, "new-host", 5432, "ecomarket")
    consistent_router.add_shard(new_shard)
    
    # Calcular redistribución
    moved_keys_consistent = 0
    for key in test_keys:
        old_shard = ConsistentHashRouter(shards, 150).get_shard(key).shard_id
        new_shard_id = consistent_router.get_shard(key).shard_id
        if old_shard != new_shard_id:
            moved_keys_consistent += 1
    
    print(f"  Keys que cambiarían de shard: {moved_keys_consistent}/{len(test_keys)} ({(moved_keys_consistent/len(test_keys)*100):.1f}%)")
    print(f"  ✅ Solo redistribuye ~25% (K/N donde N=4)!")
    
    print("\n" + "=" * 60)
    print("CONCLUSIÓN")
    print("=" * 60)
    print("Simple Hash: Fácil de implementar pero costoso escalar")
    print("Consistent Hash: Más complejo pero eficiente para elastic scaling")
    print("=" * 60)
