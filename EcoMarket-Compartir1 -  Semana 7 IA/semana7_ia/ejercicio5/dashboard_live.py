#!/usr/bin/env python3
"""
Dashboard CLI para Observabilidad en Tiempo Real
Muestra métricas de latencia, errores y throughput actualizándose cada 5s.

Uso:
    python dashboard_live.py

Requisitos:
    - API corriendo en http://localhost:8000
    - requests: pip install requests
"""

import requests
import time
import os
import sys
from datetime import datetime

API_BASE_URL = "http://localhost:8000"
REFRESH_INTERVAL = 5  # segundos


def clear_screen():
    """Limpia la pantalla según el OS."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_color(value, thresholds):
    """Retorna código ANSI color según umbral."""
    # thresholds = (yellow_limit, red_limit)
    if value > thresholds[1]:
        return "\033[91m"  # Rojo
    elif value > thresholds[0]:
        return "\033[93m"  # Amarillo
    else:
        return "\033[92m"  # Verde


def reset_color():
    """Reset color ANSI."""
    return "\033[0m"


def render_bar(value, max_value, width=30):
    """Renderiza barra de progreso ASCII."""
    filled = int((value / max_value) * width) if max_value > 0 else 0
    bar = "█" * filled + "░" * (width - filled)
    return bar


def format_endpoint(endpoint, max_length=45):
    """Trunca endpoint si es muy largo."""
    if len(endpoint) > max_length:
        return endpoint[:max_length-3] + "..."
    return endpoint.ljust(max_length)


def render_dashboard():
    """Renderiza el dashboard completo."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/_metrics", timeout=2)
        response.raise_for_status()
        data = response.json()["data"]
    except requests.exceptions.RequestException as e:
        clear_screen()
        print("=" * 80)
        print("❌ ERROR: No se pudo conectar a la API".center(80))
        print("=" * 80)
        print()
        print(f"Detalle: {e}")
        print()
        print(f"Asegúrate de que la API esté corriendo en {API_BASE_URL}")
        print("Comando: uvicorn api_observable:app --reload --port 8000")
        return
    
    clear_screen()
    
    # Header
    print("=" * 80)
    print("🔍 OBSERVABILITY DASHBOARD - LIVE METRICS".center(80))
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(80))
    print("=" * 80)
    print()
    
    # Global metrics
    global_data = data.get("_global", {})
    total_requests = global_data.get("total_requests", 0)
    uptime_seconds = global_data.get("uptime_seconds", 0)
    rps = global_data.get("requests_per_second", 0)
    
    uptime_min = uptime_seconds // 60
    uptime_sec = uptime_seconds % 60
    
    print("📊 GLOBAL METRICS")
    print("-" * 80)
    print(f"  Total Requests:  {total_requests:>10,}")
    print(f"  Uptime:          {uptime_min:>6} min {uptime_sec:>2} sec")
    print(f"  Throughput:      {rps:>10.2f} req/s")
    print()
    
    # Latency por endpoint
    print("⏱️  LATENCY & ERROR RATE PER ENDPOINT")
    print("-" * 80)
    print(f"{'Endpoint':<45} {'P50':<8} {'P95':<8} {'P99':<8} {'4xx%':<8} {'5xx%':<6}")
    print("-" * 80)
    
    endpoints = [k for k in data.keys() if k != "_global"]
    
    if not endpoints:
        print("  No endpoints with traffic yet...")
    else:
        for endpoint in sorted(endpoints):
            metrics = data[endpoint]
            latency = metrics.get("latency", {})
            errors = metrics.get("errors", {})
            
            p50 = latency.get("p50", 0)
            p95 = latency.get("p95", 0)
            p99 = latency.get("p99", 0)
            
            error_4xx = errors.get("error_rate_4xx", 0)
            error_5xx = errors.get("error_rate_5xx", 0)
            
            # Colores según umbrales
            # Latency: amarillo si p95>30ms, rojo si p95>50ms
            latency_color = get_color(p95, (30, 50))
            
            # Errors 5xx: amarillo si >0.5%, rojo si >1%
            error_color = get_color(error_5xx, (0.5, 1.0))
            
            endpoint_short = format_endpoint(endpoint, 45)
            
            print(f"{endpoint_short} "
                  f"{latency_color}{p50:>6.1f}ms{reset_color()} "
                  f"{latency_color}{p95:>6.1f}ms{reset_color()} "
                  f"{latency_color}{p99:>6.1f}ms{reset_color()} "
                  f"{error_4xx:>6.1f}% "
                  f"{error_color}{error_5xx:>5.1f}%{reset_color()}")
            
            # Barra de latencia visual
            bar = render_bar(p95, 100, width=40)
            print(f"  └─ {bar} {p95:.1f}ms / 100ms")
    
    print()
    
    # Alertas activas
    print("🚨 ACTIVE ALERTS")
    print("-" * 80)
    
    alerts = []
    
    for endpoint in endpoints:
        metrics = data[endpoint]
        latency = metrics.get("latency", {})
        errors = metrics.get("errors", {})
        
        p95 = latency.get("p95", 0)
        error_5xx = errors.get("error_rate_5xx", 0)
        error_4xx = errors.get("error_rate_4xx", 0)
        
        # Alerta 1: P95 > 50ms
        if p95 > 50:
            alerts.append(f"  ⚠️  HIGH LATENCY: {endpoint} has p95={p95:.1f}ms (threshold: 50ms)")
        
        # Alerta 2: 5xx > 1%
        if error_5xx > 1.0:
            alerts.append(f"  🔴 CRITICAL: {endpoint} has {error_5xx:.1f}% 5xx errors (threshold: 1%)")
        
        # Alerta 3: 4xx > 15% en POST /products
        if "POST" in endpoint and "/products" in endpoint and error_4xx > 15.0:
            alerts.append(f"  ⚠️  HIGH 4xx RATE: {endpoint} has {error_4xx:.1f}% validation errors (threshold: 15%)")
    
    if alerts:
        for alert in alerts:
            print(alert)
    else:
        print("  ✅ No active alerts - All systems operational")
    
    print()
    print("=" * 80)
    print(f"Refreshing in {REFRESH_INTERVAL}s... (Press Ctrl+C to exit)".center(80))


def main():
    """Loop principal del dashboard."""
    print("Starting dashboard...")
    print(f"Connecting to {API_BASE_URL}...")
    
    try:
        while True:
            render_dashboard()
            time.sleep(REFRESH_INTERVAL)
    
    except KeyboardInterrupt:
        clear_screen()
        print()
        print("=" * 80)
        print("Dashboard stopped.".center(80))
        print("=" * 80)
        print()
        sys.exit(0)


if __name__ == "__main__":
    main()
