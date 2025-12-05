#!/usr/bin/env python3
"""
🧪 TESTER DE API ECOMARKET
Script para probar la API desde VS Code de forma interactiva
"""

import requests
import json
import time
from datetime import datetime

# 🔧 Configuración
BASE_URL = "http://127.0.0.1:8000"

def print_banner():
    print("="*60)
    print("🧪 TESTER DE API ECOMARKET")
    print("="*60)
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
    print(f"🔗 URL Base: {BASE_URL}")
    print()

def test_connection():
    """Prueba la conexión básica con la API"""
    print("🔍 TESTING: Conexión básica...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API conectada correctamente")
            return True
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def get_products():
    """Obtiene y muestra todos los productos"""
    print("📦 TESTING: Obtener productos...")
    try:
        response = requests.get(f"{BASE_URL}/api/productos")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ {len(products)} productos encontrados:")
            for product in products[:3]:  # Mostrar solo los primeros 3
                print(f"   - {product['nombre']}: ${product['precio']} (Stock: {product['stock']})")
            return products
        else:
            print(f"❌ Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_connection_status():
    """Obtiene el estado de las conexiones"""
    print("🔗 TESTING: Estado de conexiones...")
    try:
        response = requests.get(f"{BASE_URL}/api/estado-conexiones")
        if response.status_code == 200:
            data = response.json()
            connections = data['conexiones']
            print("✅ Estado de servicios:")
            for service, status in connections.items():
                status_icon = "🟢" if status else "🔴"
                print(f"   {status_icon} {service}: {'ON' if status else 'OFF'}")
            return connections
        else:
            print(f"❌ Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_purchase(product_id=1, mode="HTTP_DIRECTO", cantidad=1):
    """Prueba una compra con el modo especificado"""
    print(f"🛒 TESTING: Compra - Modo {mode}...")
    try:
        purchase_data = {
            "producto_id": product_id,
            "cantidad": cantidad,
            "modo": mode
        }
        
        response = requests.post(
            f"{BASE_URL}/api/compras",
            headers={"Content-Type": "application/json"},
            json=purchase_data
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('estado') == 'fallida':
                print(f"⚠️ Compra fallida: {data.get('alerta', 'Sin detalles')}")
                if data.get('recomendacion'):
                    print(f"💡 Recomendación: {data['recomendacion']}")
            else:
                print(f"✅ Compra exitosa: ${data.get('total_pagado', 'N/A')}")
                print(f"📋 Modo: {data.get('modo_procesamiento', mode)}")
                if data.get('tiempo_total'):
                    print(f"⏱️ Tiempo total: {data['tiempo_total']}")
            return data
        else:
            error_data = response.json()
            print(f"❌ Error {response.status_code}: {error_data}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def toggle_service(service_name, active=True):
    """Activa/desactiva un servicio"""
    action = "activar" if active else "desactivar"
    print(f"🔧 TESTING: {action.capitalize()} servicio {service_name}...")
    try:
        data = {
            "servicio": service_name,
            "activo": active
        }
        
        response = requests.post(
            f"{BASE_URL}/api/simular-fallo",
            headers={"Content-Type": "application/json"},
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['mensaje']}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_all_modes():
    """Prueba todos los modos de venta disponibles"""
    modes = [
        "HTTP_DIRECTO",
        "REINTENTOS_SIMPLES", 
        "BACKOFF_EXPONENCIAL",
        "REINTENTOS_SOFISTICADOS",
        "REDIS_QUEUE",
        "RABBITMQ"
    ]
    
    print("🚀 TESTING: Todos los modos de venta...")
    results = {}
    
    for mode in modes:
        print(f"\n--- Probando {mode} ---")
        result = test_purchase(product_id=1, mode=mode, cantidad=1)
        results[mode] = result
        time.sleep(1)  # Pausa entre pruebas
    
    return results

def run_comprehensive_test():
    """Ejecuta una prueba completa del sistema"""
    print_banner()
    
    # 1. Probar conexión
    if not test_connection():
        print("❌ No se pudo conectar con la API")
        return
    
    print("\n" + "-"*50)
    
    # 2. Obtener productos
    products = get_products()
    if not products:
        print("❌ No se pudieron obtener productos")
        return
    
    print("\n" + "-"*50)
    
    # 3. Verificar estado de servicios
    connections = get_connection_status()
    
    print("\n" + "-"*50)
    
    # 4. Probar una compra simple
    print("🛒 TESTING: Compra simple...")
    test_purchase(product_id=1, mode="HTTP_DIRECTO")
    
    print("\n" + "-"*50)
    
    # 5. Probar reintentos sofisticados
    print("🎯 TESTING: Reintentos sofisticados...")
    test_purchase(product_id=1, mode="REINTENTOS_SOFISTICADOS")
    
    print("\n" + "="*60)
    print("✅ TESTING COMPLETO")
    print("="*60)

if __name__ == "__main__":
    # Ejecutar prueba rápida
    run_comprehensive_test()
    
    print("\n" + "🔧 FUNCIONES DISPONIBLES:" + "\n")
    print("- test_connection()                    # Probar conexión")
    print("- get_products()                      # Obtener productos")
    print("- get_connection_status()             # Estado de servicios")
    print("- test_purchase(id, mode, cantidad)   # Probar compra")
    print("- toggle_service(name, active)        # Activar/desactivar servicio")
    print("- test_all_modes()                    # Probar todos los modos")
    print("- run_comprehensive_test()            # Prueba completa")
    print("\n💡 Ejecuta cualquiera de estas funciones en la consola de Python")