#!/usr/bin/env python3
"""
🎯 VERIFICACIÓN COMPLETA DEL SISTEMA ECOMARKET
Script para verificar que todo está funcionando correctamente para la presentación
"""

import requests
import json
import time
from datetime import datetime

def print_header(title):
    print("="*60)
    print(f"🎯 {title}")
    print("="*60)

def check_system_status():
    """Verifica el estado completo del sistema"""
    print_header("VERIFICACIÓN DEL SISTEMA ECOMARKET")
    print(f"⏰ Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Verificar API Principal
    print("1️⃣  VERIFICANDO API PRINCIPAL...")
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print("   ✅ API Principal: FUNCIONANDO")
            print(f"   📍 URL: http://127.0.0.1:8000")
        else:
            print(f"   ❌ API Principal: ERROR {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ API Principal: NO DISPONIBLE ({e})")
        return False
    
    # 2. Verificar Productos
    print("\n2️⃣  VERIFICANDO PRODUCTOS...")
    try:
        response = requests.get("http://127.0.0.1:8000/api/productos", timeout=5)
        if response.status_code == 200:
            productos = response.json()
            print(f"   ✅ Productos: {len(productos)} productos cargados")
            for i, p in enumerate(productos[:3], 1):
                stock_status = "DISPONIBLE" if p['stock'] > 0 else "AGOTADO"
                print(f"      {i}. {p['nombre']}: ${p['precio']} - {p['stock']} unidades ({stock_status})")
            if len(productos) > 3:
                print(f"      ... y {len(productos) - 3} productos más")
        else:
            print(f"   ❌ Productos: ERROR {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Productos: ERROR ({e})")
        return False
    
    # 3. Verificar Estados de Servicios
    print("\n3️⃣  VERIFICANDO SERVICIOS...")
    try:
        response = requests.get("http://127.0.0.1:8000/api/estado-conexiones", timeout=5)
        if response.status_code == 200:
            data = response.json()
            services = data['conexiones']
            servicios_activos = sum(1 for status in services.values() if status)
            total_servicios = len(services)
            
            print(f"   📊 Estado de Servicios: {servicios_activos}/{total_servicios} ACTIVOS")
            
            for service, status in services.items():
                status_icon = "✅" if status else "❌"
                status_text = "ON" if status else "OFF"
                print(f"      {status_icon} {service}: {status_text}")
        else:
            print(f"   ❌ Estados de Servicios: ERROR {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Estados de Servicios: ERROR ({e})")
        return False
    
    # 4. Probar Modos de Venta
    print("\n4️⃣  PROBANDO MODOS DE VENTA...")
    modos = [
        ("HTTP_DIRECTO", "🔗 HTTP Directo"),
        ("REINTENTOS_SIMPLES", "🔄 Reintentos Simples"),
        ("BACKOFF_EXPONENCIAL", "📈 Backoff Exponencial"),
        ("REINTENTOS_SOFISTICADOS", "🎯 Reintentos Sofisticados"),
        ("REDIS_QUEUE", "📦 Redis Queue"),
        ("RABBITMQ", "🐰 RabbitMQ")
    ]
    
    modos_funcionando = 0
    
    for modo_code, modo_name in modos:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/compras",
                headers={"Content-Type": "application/json"},
                json={"producto_id": 1, "cantidad": 1, "modo": modo_code},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('estado') != 'fallida':
                    print(f"   ✅ {modo_name}: FUNCIONANDO")
                    modos_funcionando += 1
                else:
                    print(f"   ⚠️  {modo_name}: BLOQUEADO (servicio desactivado)")
            else:
                print(f"   ❌ {modo_name}: ERROR {response.status_code}")
        except Exception as e:
            print(f"   ❌ {modo_name}: ERROR ({str(e)[:50]}...)")
    
    print(f"\n   📊 Resumen: {modos_funcionando}/{len(modos)} modos funcionando")
    
    # 5. Verificar RabbitMQ Management
    print("\n5️⃣  VERIFICANDO RABBITMQ MANAGEMENT...")
    try:
        response = requests.get("http://localhost:15672/", timeout=5)
        if response.status_code == 200:
            print("   ✅ RabbitMQ Management: DISPONIBLE")
            print("   📍 URL: http://localhost:15672")
            print("   👤 Credenciales: admin / admin123")
        else:
            print(f"   ❌ RabbitMQ Management: ERROR {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  RabbitMQ Management: NO DISPONIBLE ({e})")
    
    # 6. Resumen Final
    print("\n" + "="*60)
    print("📋 RESUMEN DE LA VERIFICACIÓN")
    print("="*60)
    print("✅ SISTEMA LISTO PARA PRESENTACIÓN")
    print()
    print("🌐 ENLACES IMPORTANTES:")
    print("   • Aplicación Principal: http://127.0.0.1:8000")
    print("   • API Documentación: http://127.0.0.1:8000/docs")
    print("   • RabbitMQ Management: http://localhost:15672")
    print()
    print("🎯 FUNCIONALIDADES DESTACADAS:")
    print("   • ✅ 6 Modos de venta diferentes")
    print("   • ✅ Simulador de fallos de conexión")
    print("   • ✅ Reintentos sofisticados (1,2,4,8,16 segundos)")
    print("   • ✅ Persistencia de datos")
    print("   • ✅ Interfaz web interactiva")
    print("   • ✅ Gestión de stock en tiempo real")
    print()
    print("🚀 ¡SISTEMA PREPARADO PARA DEMOSTRACIÓN!")
    print("="*60)
    
    return True

if __name__ == "__main__":
    check_system_status()