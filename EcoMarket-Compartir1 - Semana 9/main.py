# 📚 IMPORTACIONES - Trae herramientas que necesitamos de otros archivos/librerías

# 🔐 CARGAR VARIABLES DE ENTORNO - DEBE SER LO PRIMERO
from dotenv import load_dotenv
load_dotenv()  # Carga variables del archivo .env

# 🚀 FastAPI: Framework principal para crear la API web
from fastapi import FastAPI, HTTPException, Depends

# 📄 Respuestas: HTMLResponse = páginas web
from fastapi.responses import HTMLResponse

# 🌐 CORS: Permite que otros sitios web usen nuestra API (seguridad web)
from fastapi.middleware.cors import CORSMiddleware

# ✅ Pydantic: Valida y estructura los datos que llegan a la API
from pydantic import BaseModel, Field, ConfigDict

# 📝 Tipos: List = listas, Optional = campos opcionales
from typing import List, Optional

# 📅 Fechas: Para manejar fechas y horas
from datetime import datetime

# 🐰 RabbitMQ: Para envío de mensajes
import pika
import json

# 🔄 Para reintentos y backoff
import time
import random
import asyncio
from functools import wraps

# 📊 Para logging
import logging

# 🗃️ Para Redis (simulado con diccionario en memoria)
import threading

# 💾 Para persistencia de datos
import os
from pathlib import Path

# 🎨 Templates: Nuestras funciones que crean las páginas HTML
from web.templates import get_homepage_html, get_dashboard_html, get_catalog_html, get_admin_html, get_sales_html, get_login_html, get_jwt_demo_html

# 🔐 JWT Authentication: Sistema de autenticación con tokens
from semana8_jwt.endpoints import router as auth_router
from semana8_jwt import middleware as jwt_middleware

# ⚙️ Configuración: Carga settings desde .env
from config import settings

# 🔒 HTTPS: Middleware para redirección HTTP → HTTPS
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# 🔢 IDENTIFICADOR DE INSTANCIA - Para balanceo de carga
# Lee la variable de entorno INSTANCE_ID o usa "default"
INSTANCE_ID = os.getenv("INSTANCE_ID", "default")

# 🏗️ CREACIÓN DE LA APLICACIÓN FastAPI - El "cerebro" de todo el sistema
app = FastAPI(
    # 🏷️ Nombre que aparece en la documentación automática
    title="EcoMarket API",
    
    # 📝 Descripción que explica qué hace la API
    description=f"API moderna para gestión de productos orgánicos - Instancia: {INSTANCE_ID}",
    
    # 🔢 Número de versión para control de cambios
    version="2.0",
    
    # 📋 URL donde está la especificación técnica de la API (JSON)
    openapi_url="/openapi.json",
    
    # 📚 URL donde está la documentación interactiva (Swagger UI)
    docs_url="/docs",
    
    # ❌ Deshabilitamos la documentación alternativa (ReDoc)
    redoc_url=None
)

# 🌐 CONFIGURACIÓN CORS - Permite que otros sitios web usen nuestra API
app.add_middleware(
    # 🛡️ Middleware de CORS (Cross-Origin Resource Sharing)
    CORSMiddleware,
    
    # 🌍 Orígenes permitidos: ["*"] = TODOS los sitios (⚠️ en producción sería más restrictivo)
    allow_origins=["*"],
    
    # 🔐 Permite enviar cookies y credenciales con las peticiones
    allow_credentials=True,
    
    # 🔧 Métodos HTTP permitidos: GET, POST, PUT, DELETE, etc. (todos)
    allow_methods=["*"],
    
    # 📋 Headers permitidos en las peticiones (todos)
    allow_headers=["*"],
)

# 🔒 CONFIGURACIÓN HTTPS - Redirección HTTP → HTTPS (solo en producción)
# IMPORTANTE: Solo activar cuando el servidor está configurado para HTTPS
# En desarrollo local con HTTP, esto causaría errores
if settings.environment == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
    print("✅ Middleware HTTPS Redirect activado (producción)")

# 🔐 REGISTRO DE ROUTERS JWT - Sistema de autenticación
app.include_router(auth_router)

# 📋 MODELOS PYDANTIC - Plantillas que definen cómo deben verse los datos

# 🛍️ MODELO PRODUCT - Define la estructura COMPLETA de un producto
class Product(BaseModel):
    # 🆔 ID único del producto (número entero obligatorio)
    id: int
    
    # 🏷️ Nombre del producto (texto obligatorio con descripción para documentación)
    nombre: str = Field(..., description="Nombre del producto")
    
    # 📂 Categoría (texto obligatorio - ej: "Frutas", "Verduras")
    categoria: str = Field(..., description="Categoría del producto")
    
    # 💰 Precio (número decimal, DEBE ser mayor que 0)
    precio: float = Field(..., gt=0, description="Precio del producto (debe ser mayor que 0)")
    
    # ✅ Disponibilidad (verdadero/falso, por defecto = disponible)
    disponible: bool = Field(default=True, description="Disponibilidad del producto")
    
    # � Stock/Inventario (número de unidades disponibles, debe ser >= 0)
    stock: int = Field(default=0, ge=0, description="Cantidad en inventario (unidades disponibles)")
    
    # �📝 Descripción (texto opcional - puede ser None/vacío)
    descripcion: Optional[str] = Field(None, description="Descripción opcional del producto")
    
    # 📅 Fecha de creación (se pone automáticamente la fecha actual)
    fecha_agregado: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "nombre": "Manzana Orgánica",
                "categoria": "Frutas",
                "precio": 2.5,
                "disponible": True,
                "stock": 150,
                "descripcion": "Manzanas orgánicas frescas",
                "fecha_agregado": "2024-01-15T10:30:00"
            }
        }
    )

class ProductCreate(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del producto")
    categoria: str = Field(..., min_length=1, description="Categoría del producto")
    precio: float = Field(..., gt=0, description="Precio del producto (debe ser mayor que 0)")
    disponible: bool = Field(default=True, description="Disponibilidad del producto")
    stock: int = Field(default=0, ge=0, description="Cantidad en inventario")
    descripcion: Optional[str] = Field(None, description="Descripción opcional del producto")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Tomate Orgánico",
                "categoria": "Verduras",
                "precio": 3.0,
                "disponible": True,
                "stock": 200,
                "descripcion": "Tomates frescos cultivados orgánicamente"
            }
        }
    )

# ✏️ MODELO PRODUCT UPDATE - Para MODIFICAR productos existentes (todos los campos opcionales)
class ProductUpdate(BaseModel):
    # 🏷️ Nombre opcional (si no se envía, no se cambia, min_length=1 evita nombres vacíos)
    nombre: Optional[str] = Field(None, min_length=1, description="Nombre del producto")
    
    # 📂 Categoría opcional (si no se envía, no se cambia)
    categoria: Optional[str] = Field(None, min_length=1, description="Categoría del producto")
    
    # 💰 Precio opcional (si se envía, debe ser mayor que 0)
    precio: Optional[float] = Field(None, gt=0, description="Precio del producto (debe ser mayor que 0)")
    
    # ✅ Disponibilidad opcional (si no se envía, no se cambia)
    disponible: Optional[bool] = Field(None, description="Disponibilidad del producto")
    
    # � Stock opcional (si no se envía, no se cambia)
    stock: Optional[int] = Field(None, ge=0, description="Cantidad en inventario")
    
    # �📝 Descripción opcional (si no se envía, no se cambia)
    descripcion: Optional[str] = Field(None, description="Descripción opcional del producto")

# � MODELO COMPRA - Define la estructura de una compra
class CompraRequest(BaseModel):
    producto_id: int = Field(..., description="ID del producto a comprar")
    cantidad: int = Field(default=1, gt=0, description="Cantidad a comprar (debe ser mayor que 0)")
    modo: str = Field(..., description="Modo de procesamiento: HTTP_DIRECTO, REINTENTOS_SIMPLES, BACKOFF_EXPONENCIAL, REDIS_QUEUE, RABBITMQ")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "producto_id": 1,
                "cantidad": 2,
                "modo": "RABBITMQ"
            }
        }
    )

# � FUNCIONES DE PERSISTENCIA - Para guardar y cargar datos
DATA_FILE = "productos_data.json"

def guardar_productos():
    """Guarda los productos en un archivo JSON"""
    try:
        datos_productos = []
        for producto in productos_db:
            datos_productos.append({
                "id": producto.id,
                "nombre": producto.nombre,
                "categoria": producto.categoria,
                "precio": producto.precio,
                "disponible": producto.disponible,
                "stock": producto.stock,
                "descripcion": producto.descripcion,
                "fecha_agregado": producto.fecha_agregado.isoformat()
            })
        
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(datos_productos, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error guardando productos: {e}")

def cargar_productos():
    """Carga los productos desde el archivo JSON"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                datos_productos = json.load(f)
            
            productos_cargados = []
            for dato in datos_productos:
                producto = Product(
                    id=dato["id"],
                    nombre=dato["nombre"],
                    categoria=dato["categoria"],
                    precio=dato["precio"],
                    disponible=dato["disponible"],
                    stock=dato["stock"],
                    descripcion=dato["descripcion"],
                    fecha_agregado=datetime.fromisoformat(dato["fecha_agregado"])
                )
                productos_cargados.append(producto)
            
            return productos_cargados
        
    except Exception as e:
        print(f"Error cargando productos: {e}")
    
    return None

# �📊 BASE DE DATOS SIMULADA - Lista en memoria que actúa como base de datos
# (En producción real sería MySQL, PostgreSQL, etc.)

# Intentar cargar productos existentes, si no existen usar los por defecto
productos_cargados = cargar_productos()

if productos_cargados:
    productos_db = productos_cargados
    # Calcular el próximo ID basado en los productos cargados
    next_id = max([p.id for p in productos_db]) + 1 if productos_db else 1
else:
    # Usar productos por defecto si no hay archivo guardado
    productos_db = [
    # 🍎 Producto 1: Manzana Orgánica
    Product(
        id=1,  # ID único
        nombre="Manzana Orgánica",  # Nombre del producto
        categoria="Frutas",  # Tipo de producto
        precio=2.5,  # Precio en la moneda local
        disponible=True,  # Está en stock
        stock=150,  # Unidades disponibles en inventario
        descripcion="Manzanas orgánicas frescas y crujientes"  # Descripción detallada
    ),
    Product(
        id=2,
        nombre="Tomate Cherry",
        categoria="Verduras",
        precio=3.0,
        disponible=True,
        stock=200,
        descripcion="Tomates cherry dulces y jugosos"
    ),
    Product(
        id=3,
        nombre="Lechuga Hidropónica",
        categoria="Verduras",
        precio=1.8,
        disponible=False,
        stock=0,
        descripcion="Lechuga fresca cultivada hidropónicamente"
    ),
    Product(
        id=4,
        nombre="Zanahoria Orgánica",
        categoria="Verduras",
        precio=2.2,
        disponible=True,
        stock=300,
        descripcion="Zanahorias orgánicas ricas en vitaminas"
    ),
    Product(
        id=5,
        nombre="Palta Hass",
        categoria="Frutas",
        precio=4.5,
        disponible=True,
        stock=80,
        descripcion="Paltas Hass cremosas y nutritivas"
    )
    ]
    
    # Guardar productos por defecto la primera vez
    guardar_productos()
    
    # 🔢 CONTADOR DE IDs - Variable que lleva el control del próximo ID a asignar
    next_id = 6  # Empieza en 6 porque ya tenemos productos del 1 al 5

# 🐰 FUNCIONES RABBITMQ - Para envío de mensajes a colas
def conectar_rabbitmq():
    """Establece conexión con RabbitMQ"""
    # Verificar estado simulado de conexión
    if not connection_status.get("rabbitmq", True) or not connection_status.get("general_network", True):
        print("🚨 Simulación: Conexión a RabbitMQ deshabilitada")
        return None
    
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                virtual_host='/',
                credentials=pika.PlainCredentials('admin', 'admin123'),
                connection_attempts=3,
                retry_delay=1,
                socket_timeout=5
            )
        )
        return connection
    except pika.exceptions.AMQPConnectionError:
        print("🚨 Error: No se puede conectar a RabbitMQ. Verifica que el servicio esté ejecutándose.")
        return None
    except pika.exceptions.AuthenticationError:
        print("🚨 Error: Credenciales incorrectas para RabbitMQ.")
        return None
    except Exception as e:
        print(f"🚨 Error conectando a RabbitMQ: {e}")
        return None

def enviar_mensaje_compra(mensaje_compra):
    """Envía mensaje de compra a RabbitMQ con manejo de errores mejorado"""
    try:
        connection = conectar_rabbitmq()
        if connection is None:
            return {
                "success": False, 
                "error": "No se pudo establecer conexión con RabbitMQ",
                "error_type": "CONNECTION_ERROR",
                "message": "Verifica que RabbitMQ esté ejecutándose y las credenciales sean correctas"
            }
        
        channel = connection.channel()
        
        # Declarar la cola de compras (se crea si no existe)
        queue_name = 'compras_ecomarket'
        channel.queue_declare(queue=queue_name, durable=True)
        
        # Enviar el mensaje
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(mensaje_compra, ensure_ascii=False, default=str),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Hace el mensaje persistente
                content_type='application/json',
                timestamp=int(datetime.now().timestamp())
            )
        )
        
        connection.close()
        return {
            "success": True,
            "message": "Mensaje enviado exitosamente a RabbitMQ",
            "queue": queue_name
        }
        
    except pika.exceptions.ChannelClosedByBroker as e:
        print(f"🚨 Error: Canal cerrado por el broker RabbitMQ: {e}")
        return {
            "success": False,
            "error": "Canal cerrado por RabbitMQ",
            "error_type": "CHANNEL_ERROR", 
            "message": "El canal de comunicación fue cerrado inesperadamente"
        }
    except pika.exceptions.AMQPError as e:
        print(f"🚨 Error AMQP en RabbitMQ: {e}")
        return {
            "success": False,
            "error": "Error de protocolo AMQP",
            "error_type": "AMQP_ERROR",
            "message": "Error en el protocolo de comunicación con RabbitMQ"
        }
    except Exception as e:
        print(f"🚨 Error inesperado enviando mensaje a RabbitMQ: {e}")
        if 'connection' in locals() and connection:
            try:
                connection.close()
            except:
                pass
        return {
            "success": False,
            "error": f"Error inesperado: {str(e)}",
            "error_type": "UNEXPECTED_ERROR",
            "message": "Ocurrió un error inesperado al procesar la venta"
        }

# 🔄 FUNCIONES PARA REINTENTOS SIMPLES
def procesar_con_reintentos(mensaje_compra, max_reintentos=4):
    """Procesa la compra con reintentos simples y manejo de errores mejorado"""
    errores = []
    
    # Verificar estado específico de REINTENTOS SIMPLES
    reintentos_disabled = not connection_status.get("reintentos_simples", True)
    network_disabled = not connection_status.get("general_network", True)
    
    if reintentos_disabled or network_disabled:
        servicio_afectado = "Reintentos Simples" if reintentos_disabled else "Red General"
        
        for intento in range(1, 5):  # 4 reintentos cuando servicio está off
            print(f"🔄 Reintentos Simples - Intento {intento}/4: {servicio_afectado} desactivado")
            errores.append(f"Intento {intento}: {servicio_afectado} no disponible")
            
            if intento < 4:
                print(f"⏳ Esperando 1 segundo antes del siguiente intento...")
                time.sleep(1)
        
        return {
            "status": "failed",
            "intento": 4,
            "mensaje": f"❌ REINTENTOS SIMPLES FALLIDOS: {servicio_afectado} desactivado después de 4 intentos",
            "error_type": "REINTENTOS_SIMPLES_DISABLED",
            "errores": errores,
            "recomendacion": f"Reactiva '{servicio_afectado}' desde el simulador de fallos"
        }
    
    for intento in range(1, max_reintentos + 1):
        try:
            # Verificar estado específico de REINTENTOS SIMPLES en cada intento
            if not connection_status.get("reintentos_simples", True):
                raise ConnectionError("Servicio de Reintentos Simples desactivado")
            
            # Simular diferentes tipos de errores de conexión
            probabilidad = random.random()
            
            if probabilidad < 0.15:  # 15% Error de conexión
                raise ConnectionError("Error de conexión de red")
            elif probabilidad < 0.25:  # 10% Error de timeout
                raise TimeoutError("Timeout en la conexión")
            elif probabilidad < 0.30:  # 5% Error de servicio no disponible
                raise Exception("Servicio temporalmente no disponible")
            elif probabilidad < 0.70:  # 40% Éxito
                print(f"✅ Compra procesada exitosamente en intento {intento}")
                return {
                    "status": "success", 
                    "intento": intento, 
                    "mensaje": f"✅ Procesado exitosamente en intento {intento}/{max_reintentos}",
                    "detalles": f"Compra completada después de {intento} intento(s)"
                }
            else:  # 30% Error genérico
                raise Exception("Error interno del servidor")
                
        except ConnectionError as e:
            error_msg = f"🌐 Reintentos Simples - Error de conexión en intento {intento}: {e}"
            print(error_msg)
            errores.append(f"Intento {intento}: Error de conexión (Reintentos Simples)")
        except TimeoutError as e:
            error_msg = f"⏰ Reintentos Simples - Timeout en intento {intento}: {e}"
            print(error_msg)
            errores.append(f"Intento {intento}: Timeout (Reintentos Simples)")
        except Exception as e:
            error_msg = f"❌ Reintentos Simples - Error en intento {intento}: {e}"
            print(error_msg)
            errores.append(f"Intento {intento}: {str(e)} (Reintentos Simples)")
        
        if intento < max_reintentos:
            print(f"🔄 Reintentos Simples - Reintentando en 1 segundo... ({intento}/{max_reintentos})")
            time.sleep(1)
    
    return {
        "status": "failed", 
        "intento": max_reintentos, 
        "mensaje": f"❌ VENTA FALLIDA: No se pudo procesar después de {max_reintentos} intentos",
        "error_type": "RETRY_EXHAUSTED",
        "errores": errores,
        "recomendacion": "Verifica tu conexión a internet y vuelve a intentar más tarde"
    }

# 📈 FUNCIONES PARA BACKOFF EXPONENCIAL
def procesar_con_backoff_exponencial(mensaje_compra, max_reintentos=5):
    """Procesa la compra con backoff exponencial y manejo de errores avanzado"""
    errores = []
    tiempos_espera = []
    
    # Verificar estado específico de BACKOFF EXPONENCIAL
    backoff_disabled = not connection_status.get("backoff_exponencial", True)
    network_disabled = not connection_status.get("general_network", True)
    
    if backoff_disabled or network_disabled:
        servicio_afectado = "Backoff Exponencial" if backoff_disabled else "Red General"
        
        for intento in range(1, 5):  # 4 reintentos cuando servicio está off
            print(f"🔄 Backoff Exponencial - Intento {intento}/4: {servicio_afectado} desactivado")
            errores.append(f"Intento {intento}: {servicio_afectado} no disponible")
            
            if intento < 4:
                # Backoff exponencial acelerado para demo: 0.5, 1, 1.5 segundos
                delay = min(0.5 * (2 ** (intento-1)), 1.5)  # Máximo 1.5 segundos para demo
                tiempos_espera.append(delay)
                print(f"⏳ Backoff exponencial: esperando {delay} segundos...")
                time.sleep(delay)
        
        tiempo_total = sum(tiempos_espera)
        return {
            "status": "failed",
            "intento": 4,
            "mensaje": f"❌ BACKOFF EXPONENCIAL FALLIDO: {servicio_afectado} desactivado después de 4 intentos",
            "error_type": "BACKOFF_EXPONENCIAL_DISABLED",
            "tiempo_total_esperas": f"{tiempo_total:.1f} segundos",
            "errores": errores,
            "recomendacion": f"Reactiva '{servicio_afectado}' desde el simulador de fallos"
        }
    
    for intento in range(1, max_reintentos + 1):
        try:
            # Verificar estado específico de BACKOFF EXPONENCIAL en cada intento  
            if not connection_status.get("backoff_exponencial", True):
                raise ConnectionError("Servicio de Backoff Exponencial desactivado")
            
            # Simular diferentes tipos de errores con probabilidades realistas
            probabilidad = random.random()
            
            if probabilidad < 0.20:  # 20% Error de conexión
                raise ConnectionError("Conexión perdida con el servidor")
            elif probabilidad < 0.30:  # 10% Error de sobrecarga del servidor
                raise Exception("Servidor sobrecargado")
            elif probabilidad < 0.35:  # 5% Error de timeout
                raise TimeoutError("Timeout en la respuesta del servidor")
            elif probabilidad < 0.60:  # 25% Éxito
                tiempo_total = sum(tiempos_espera)
                print(f"✅ Compra procesada con backoff exponencial en intento {intento}")
                return {
                    "status": "success", 
                    "intento": intento, 
                    "mensaje": f"✅ Procesado exitosamente con backoff exponencial en intento {intento}",
                    "tiempo_total_esperas": f"{tiempo_total:.1f} segundos",
                    "detalles": f"Completado después de {len(tiempos_espera)} esperas"
                }
            else:  # 40% Error de servicio
                raise Exception("Error interno del servicio de pagos")
                
        except ConnectionError as e:
            error_msg = f"🌐 Backoff Exponencial - Error de conexión en intento {intento}: {e}"
            print(error_msg)
            errores.append(f"Intento {intento}: Error de conexión (Backoff Exponencial)")
        except TimeoutError as e:
            error_msg = f"⏰ Backoff Exponencial - Timeout en intento {intento}: {e}"
            print(error_msg)
            errores.append(f"Intento {intento}: Timeout (Backoff Exponencial)")
        except Exception as e:
            error_msg = f"❌ Backoff Exponencial - Error en intento {intento}: {e}"
            print(error_msg)
            errores.append(f"Intento {intento}: {str(e)} (Backoff Exponencial)")
        
        if intento < max_reintentos:
            # Backoff exponencial acelerado para demo: 0.5s, 1s, 1.5s, 2s...
            delay = min(0.5 * (2 ** (intento-1)), 2)  # Máximo 2 segundos para demo
            tiempos_espera.append(delay)
            print(f"🔄 Backoff Exponencial - esperando {delay} segundos antes del intento {intento + 1}/{max_reintentos}...")
            time.sleep(delay)
    
    tiempo_total = sum(tiempos_espera)
    return {
        "status": "failed", 
        "intento": max_reintentos, 
        "mensaje": f"❌ VENTA FALLIDA: Backoff exponencial agotado después de {max_reintentos} intentos",
        "error_type": "BACKOFF_EXHAUSTED",
        "tiempo_total_esperas": f"{tiempo_total:.1f} segundos",
        "errores": errores,
        "recomendacion": "El sistema está experimentando problemas. Intenta nuevamente en unos minutos o contacta soporte técnico"
    }

# 🎯 FUNCIONES PARA REINTENTOS SOFISTICADOS
def procesar_con_reintentos_sofisticados(mensaje_compra, max_reintentos=5):
    """Procesa la compra con reintentos sofisticados - tiempos específicos: 1, 2, 4, 8, 16 segundos"""
    errores = []
    tiempos_espera = [1, 2, 4, 8, 16]  # Tiempos específicos para cada reintento (1-5)
    tiempo_total_usado = 0
    
    # Verificar estado específico de REINTENTOS SOFISTICADOS
    sofisticados_disabled = not connection_status.get("reintentos_sofisticados", True)
    network_disabled = not connection_status.get("general_network", True)
    
    if sofisticados_disabled or network_disabled:
        servicio_afectado = "Reintentos Sofisticados" if sofisticados_disabled else "Red General"
        
        for intento in range(1, 6):  # 5 intentos cuando servicio está off
            delay = tiempos_espera[intento - 1]  # Tiempo para este intento específico
            print(f"🎯 Reintentos Sofisticados - Intento {intento}/5: {servicio_afectado} desactivado - Esperando {delay}s")
            errores.append(f"Intento {intento}: {servicio_afectado} no disponible (espera {delay}s)")
            
            time.sleep(delay)
            tiempo_total_usado += delay
        
        return {
            "status": "failed",
            "intento": 5,
            "mensaje": f"❌ REINTENTOS SOFISTICADOS FALLIDOS: {servicio_afectado} desactivado después de 5 intentos",
            "error_type": "REINTENTOS_SOFISTICADOS_DISABLED",
            "tiempo_total_esperas": f"{tiempo_total_usado} segundos",
            "errores": errores,
            "recomendacion": f"Reactiva '{servicio_afectado}' desde el simulador de fallos"
        }
    
    # Procesar con reintentos sofisticados cuando el servicio está activo
    for intento in range(1, max_reintentos + 1):
        delay = tiempos_espera[intento - 1]  # Tiempo para este intento específico
        print(f"🎯 Reintentos Sofisticados - Intento {intento}/5 (espera programada: {delay}s)")
        
        # Aplicar la espera específica para este intento
        time.sleep(delay)
        tiempo_total_usado += delay
        
        try:
            # Verificar estado específico de REINTENTOS SOFISTICADOS en cada intento
            if not connection_status.get("reintentos_sofisticados", True):
                raise ConnectionError("Servicio de Reintentos Sofisticados desactivado")
            
            # Simular diferentes tipos de errores con probabilidades realistas
            probabilidad = random.random()
            
            if probabilidad < 0.18:  # 18% Error de conexión
                raise ConnectionError("Error de conexión de red sofisticada")
            elif probabilidad < 0.28:  # 10% Error de timeout
                raise TimeoutError("Timeout en conexión sofisticada")
            elif probabilidad < 0.33:  # 5% Error de servicio no disponible
                raise Exception("Servicio sofisticado temporalmente no disponible")
            elif probabilidad < 0.65:  # 32% Éxito
                print(f"✅ Compra procesada exitosamente con Reintentos Sofisticados en intento {intento} (después de {tiempo_total_usado}s)")
                return {
                    "status": "success", 
                    "intento": intento, 
                    "mensaje": f"✅ Procesado exitosamente con Reintentos Sofisticados en intento {intento}/5",
                    "detalles": f"Compra completada después de {intento} intento(s) y {tiempo_total_usado} segundos",
                    "tiempo_total_esperas": f"{tiempo_total_usado} segundos"
                }
            else:  # 35% Error genérico
                raise Exception("Error interno del servidor sofisticado")
                
        except ConnectionError as e:
            error_msg = f"🌐 Reintentos Sofisticados - Error de conexión en intento {intento} (tras {delay}s): {e}"
            print(error_msg)
            errores.append(f"Intento {intento}: Error de conexión tras esperar {delay}s")
        except TimeoutError as e:
            error_msg = f"⏰ Reintentos Sofisticados - Timeout en intento {intento} (tras {delay}s): {e}"
            print(error_msg)
            errores.append(f"Intento {intento}: Timeout tras esperar {delay}s")
        except Exception as e:
            error_msg = f"❌ Reintentos Sofisticados - Error en intento {intento} (tras {delay}s): {e}"
            print(error_msg)
            errores.append(f"Intento {intento}: {str(e)} tras esperar {delay}s")
    
    return {
        "status": "failed", 
        "intento": max_reintentos, 
        "mensaje": f"❌ VENTA FALLIDA: Reintentos Sofisticados agotados después de 5 intentos y {tiempo_total_usado} segundos",
        "error_type": "REINTENTOS_SOFISTICADOS_EXHAUSTED",
        "tiempo_total_esperas": f"{tiempo_total_usado} segundos",
        "errores": errores,
        "recomendacion": "El sistema sofisticado está experimentando problemas. Intenta nuevamente más tarde"
    }

# 📦 SIMULADOR DE REDIS QUEUE
# En un entorno real, usarías redis-py para conectarte a Redis
redis_queue = []
redis_lock = threading.Lock()

def agregar_a_redis_queue(mensaje_compra):
    """Simula agregar mensaje a cola Redis con manejo de errores"""
    try:
        # Verificar estado simulado de conexión
        if not connection_status.get("redis", True) or not connection_status.get("general_network", True):
            raise ConnectionError("Conexión a Redis deshabilitada (simulación)")
            
        # Simular posibles errores de conexión a Redis
        if random.random() < 0.1:  # 10% probabilidad de error
            raise ConnectionError("No se pudo conectar a Redis")
        
        with redis_lock:
            mensaje_con_id = {
                "id": len(redis_queue) + 1,
                "timestamp": datetime.now().isoformat(),
                **mensaje_compra
            }
            redis_queue.append(mensaje_con_id)
            print(f"📦 Mensaje agregado a Redis Queue (simulada). Total en cola: {len(redis_queue)}")
            return {
                "status": "queued", 
                "queue_id": mensaje_con_id["id"], 
                "queue_size": len(redis_queue),
                "success": True,
                "message": "Venta agregada exitosamente a la cola de procesamiento"
            }
    
    except ConnectionError as e:
        print(f"🚨 Error de conexión a Redis: {e}")
        return {
            "status": "failed",
            "success": False,
            "error": "No se pudo conectar a Redis",
            "error_type": "REDIS_CONNECTION_ERROR",
            "message": "La venta no pudo ser procesada. Verifica la conexión a Redis.",
            "recomendacion": "Intenta con otro modo de procesamiento o contacta al administrador"
        }
    except Exception as e:
        print(f"🚨 Error inesperado en Redis Queue: {e}")
        return {
            "status": "failed",
            "success": False,
            "error": f"Error inesperado: {str(e)}",
            "error_type": "REDIS_UNEXPECTED_ERROR",
            "message": "Ocurrió un error inesperado al procesar la venta en Redis",
            "recomendacion": "Intenta nuevamente o usa otro modo de procesamiento"
        }

def procesar_redis_queue():
    """Simula procesamiento de cola Redis"""
    with redis_lock:
        if redis_queue:
            mensaje = redis_queue.pop(0)
            print(f"🔄 Procesando mensaje {mensaje['id']} de Redis Queue")
            return {"status": "processed", "mensaje": mensaje}
        return {"status": "empty", "mensaje": "Cola vacía"}

# ----- Datos y endpoints para la ventana de acciones (modos / registros)
modes = [
    {"id": 1, "name": "HTTP Directo"},
    {"id": 2, "name": "Reintentos Simples"},
    {"id": 3, "name": "Backoff Exponencial"},
    {"id": 4, "name": "Redis Queue (En Redis)"},
    {"id": 5, "name": "RabbitMQ (Garantías)"}
]

registrations = []

# 🧪 SIMULADOR DE FALLOS DE CONEXIÓN - Para testing
connection_status = {
    "rabbitmq": True,
    "redis": True,
    "http_directo": True,
    "reintentos_simples": True,
    "backoff_exponencial": True,
    "reintentos_sofisticados": True,
    "general_network": True
}

@app.post("/api/simular-fallo")
async def simular_fallo_conexion(fallo: dict):
    """Simula fallos de conexión para testing"""
    servicio = fallo.get("servicio", "").lower()
    estado = fallo.get("activo", False)  # True = activo, False = desactivado
    
    if servicio in connection_status:
        connection_status[servicio] = estado
        accion = "activado" if estado else "desactivado"
        print(f"🔄 {servicio.upper()} -> {'ON' if estado else 'OFF'}")
        return {
            "servicio": servicio,
            "nuevo_estado": estado,
            "mensaje": f"Servicio {servicio} {accion}",
            "estado_actual": connection_status
        }
    
    return {
        "error": f"Servicio '{servicio}' no reconocido",
        "servicios_disponibles": list(connection_status.keys())
    }

@app.post("/api/reset-conexiones")
async def reset_conexiones():
    """Resetea todas las conexiones a estado activo"""
    global connection_status
    for service in connection_status:
        connection_status[service] = True
    print("🔄 RESET: Todos los servicios reactivados")
    return {
        "mensaje": "Todas las conexiones han sido reactivadas",
        "estado_actual": connection_status
    }

@app.get("/api/estado-conexiones")  
async def obtener_estado_conexiones():
    """Obtiene el estado actual de las conexiones simuladas"""
    return {
        "conexiones": connection_status,
        "descripcion": {
            "rabbitmq": "Estado de conexión a RabbitMQ (solo afecta modo RabbitMQ)",
            "redis": "Estado de conexión a Redis (solo afecta modo Redis Queue)",
            "http_directo": "Estado de conexión HTTP Directo (solo afecta modo HTTP Directo)",
            "reintentos_simples": "Estado de servicio Reintentos Simples (solo afecta modo Reintentos Simples)",
            "backoff_exponencial": "Estado de servicio Backoff Exponencial (solo afecta modo Backoff Exponencial)",
            "general_network": "Estado general de la red (afecta TODOS los modos)"
        },
        "impacto_por_modo": {
            "HTTP_DIRECTO": ["http_directo", "general_network"],
            "REINTENTOS_SIMPLES": ["reintentos_simples", "general_network"],
            "BACKOFF_EXPONENCIAL": ["backoff_exponencial", "general_network"],
            "REDIS_QUEUE": ["redis", "general_network"],
            "RABBITMQ": ["rabbitmq", "general_network"]
        }
    }

@app.post("/api/test-connection-retry")
async def test_connection_with_retry():
    """Endpoint para probar específicamente los reintentos con el estado del simulador"""
    mensaje_prueba = {
        "test": True,
        "timestamp": datetime.now().isoformat()
    }
    
    # Probar reintentos simples
    resultado_reintentos = procesar_con_reintentos(mensaje_prueba)
    
    # Probar backoff exponencial  
    resultado_backoff = procesar_con_backoff_exponencial(mensaje_prueba)
    
    # Probar reintentos sofisticados
    resultado_sofisticados = procesar_con_reintentos_sofisticados(mensaje_prueba)
    
    return {
        "estado_conexiones": connection_status,
        "reintentos_simples": resultado_reintentos,
        "backoff_exponencial": resultado_backoff,
        "reintentos_sofisticados": resultado_sofisticados
    }

@app.post("/api/desactivar-todo")
async def desactivar_todos_servicios():
    """Desactiva todos los servicios para testing"""
    global connection_status
    for servicio in connection_status:
        connection_status[servicio] = False
    
    return {
        "mensaje": "🚨 TODOS los servicios han sido DESACTIVADOS",
        "estado_actual": connection_status
    }

@app.post("/api/activar-todo") 
async def activar_todos_servicios():
    """Activa todos los servicios"""
    global connection_status
    for servicio in connection_status:
        connection_status[servicio] = True
    
    return {
        "mensaje": "✅ TODOS los servicios han sido ACTIVADOS",
        "estado_actual": connection_status
    }


@app.get("/api/modos")
async def get_modos():
    """Retorna los modos disponibles para la ventana de Acciones"""
    return modes


@app.post("/api/acciones/register")
async def register_action(payload: dict):
    """Registra una acción simple (simulada) y la guarda en memoria"""
    mode_id = payload.get('mode_id')
    action = payload.get('action', 'change_mode')
    modo = next((m for m in modes if m['id'] == mode_id), None)
    if modo is None:
        raise HTTPException(status_code=400, detail="Modo inválido")

    record = {
        'id': len(registrations) + 1,
        'mode_id': mode_id,
        'mode_name': modo['name'],
        'action': action,
        'timestamp': datetime.now().isoformat()
    }
    registrations.append(record)

    return {"mensaje": f"Acción registrada: {action} en modo {modo['name']}", "registro": record}

# � HEALTH CHECK - Endpoint para que el balanceador verifique si la instancia está saludable
@app.get("/health")
async def health_check():
    """
    🩺 Health Check Endpoint
    - Usado por Nginx para verificar si esta instancia está funcionando
    - Retorna estado, ID de instancia y timestamp
    """
    return {
        "status": "healthy",
        "instance_id": INSTANCE_ID,
        "timestamp": datetime.now().isoformat(),
        "service": "EcoMarket API"
    }

# 🔍 ENDPOINT DE INFORMACIÓN DE INSTANCIA
@app.get("/api/instance-info")
async def instance_info():
    """
    📋 Información de la instancia actual
    - Útil para verificar qué instancia está procesando el request
    """
    return {
        "instance_id": INSTANCE_ID,
        "timestamp": datetime.now().isoformat(),
        "endpoints": ["/health", "/api/instance-info", "/", "/dashboard"]
    }

# �🌐 RUTAS DE LA INTERFAZ WEB - Endpoints que devuelven páginas HTML (para humanos)

# 🏠 RUTA PRINCIPAL - Cuando alguien visita http://localhost:8000/
@app.get("/", response_class=HTMLResponse)
async def homepage():
    """📄 Función que devuelve la página principal como HTML"""
    # 🎯 Llama a la función que genera el HTML y lo devuelve con código 200 (OK)
    return HTMLResponse(content=get_homepage_html(), status_code=200)

# 📊 RUTA DASHBOARD - Página con gráficos y estadísticas
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """📈 Función que devuelve la página del dashboard con gráficos"""
    return HTMLResponse(content=get_dashboard_html(), status_code=200)

# 🛍️ RUTA CATÁLOGO - Página que muestra todos los productos
@app.get("/catalog", response_class=HTMLResponse)
async def catalog():
    """🛒 Función que devuelve la página del catálogo de productos"""
    return HTMLResponse(content=get_catalog_html(), status_code=200)

# 📊 RUTA ALTERNATIVA DASHBOARD - Para los enlaces que usan /stats-dashboard
@app.get("/stats-dashboard", response_class=HTMLResponse)
async def stats_dashboard():
    """📈 Función alternativa que devuelve la página del dashboard con gráficos"""
    return HTMLResponse(content=get_dashboard_html(), status_code=200)

# 🛒 RUTA ALTERNATIVA CATÁLOGO - Para los enlaces que usan /products-catalog
@app.get("/products-catalog", response_class=HTMLResponse)
async def products_catalog():
    """🛍️ Función alternativa que devuelve la página del catálogo de productos"""
    return HTMLResponse(content=get_catalog_html(), status_code=200)

# 🔐 RUTA LOGIN - Página de inicio de sesión
@app.get("/login", response_class=HTMLResponse)
async def login_page():
    """🔐 Función que devuelve la página de login"""
    return HTMLResponse(content=get_login_html(), status_code=200)

# 🔒 RUTA JWT DEMO - Demostración interactiva de JWT + HTTPS
@app.get("/jwt-demo", response_class=HTMLResponse)
async def jwt_demo_page():
    """🔒 Página de demostración interactiva de JWT + HTTPS + Gestión de Secretos"""
    return HTMLResponse(content=get_jwt_demo_html(), status_code=200)

# 🔧 RUTA ADMIN - Página de administración de productos
@app.get("/admin", response_class=HTMLResponse)
async def admin():
    """🔧 Función que devuelve la página de administración de productos"""
    return HTMLResponse(content=get_admin_html(), status_code=200)

# 🔒 RUTA ESTADO DE SEGURIDAD - Muestra información de JWT, HTTPS y Secretos
@app.get("/security-status")
async def security_status():
    """🔒 Endpoint que muestra el estado de todas las implementaciones de seguridad"""
    import os
    from datetime import datetime
    
    # Verificar si estamos en HTTPS
    https_enabled = os.path.exists("certs/cert.pem") and os.path.exists("certs/key.pem")
    
    # Información de certificado
    cert_info = None
    if https_enabled:
        try:
            from cryptography import x509
            from cryptography.hazmat.primitives import serialization
            
            with open("certs/cert.pem", "rb") as f:
                cert = x509.load_pem_x509_certificate(f.read())
                cert_info = {
                    "issuer": cert.issuer.rfc4514_string(),
                    "subject": cert.subject.rfc4514_string(),
                    "valid_from": cert.not_valid_before_utc.isoformat(),
                    "valid_until": cert.not_valid_after_utc.isoformat(),
                    "key_size": cert.public_key().key_size if hasattr(cert.public_key(), 'key_size') else "N/A",
                    "serial_number": cert.serial_number
                }
        except Exception as e:
            cert_info = {"error": str(e)}
    
    return {
        "timestamp": datetime.now().isoformat(),
        "security_layers": {
            "jwt_authentication": {
                "status": "✅ Implementado",
                "features": {
                    "algorithm": settings.jwt_algorithm,
                    "token_expiration_minutes": settings.jwt_expire_minutes,
                    "refresh_tokens": "✅ Habilitado (7 días)",
                    "logout_revocation": "✅ Implementado",
                    "roles": ["admin", "vendedor", "cliente"],
                    "protected_endpoints": 3,
                    "tests": "✅ 30 tests automatizados"
                },
                "week": "Semana 8"
            },
            "https_tls": {
                "status": "✅ Implementado" if https_enabled else "⚠️ No habilitado",
                "features": {
                    "port": 8443 if https_enabled else 8001,
                    "protocol": "HTTPS" if https_enabled else "HTTP",
                    "certificate": cert_info if https_enabled else "No configurado",
                    "redirect_middleware": f"✅ Configurado (activo en producción)"
                },
                "week": "Semana 9"
            },
            "secrets_management": {
                "status": "✅ Implementado",
                "features": {
                    "config_system": "pydantic-settings",
                    "env_file": "✅ .env (gitignored)",
                    "validation": "✅ Automática",
                    "jwt_secret_length": len(settings.jwt_secret),
                    "secrets_different": settings.jwt_secret != settings.jwt_refresh_secret,
                    "environment": settings.environment
                },
                "week": "Semana 9"
            }
        },
        "overall_status": "✅ Sistema Seguro - Hito 2 Completo",
        "documentation": {
            "https_setup": "/HTTPS_SETUP.md",
            "jwt_readme": "/semana8_jwt/README.md",
            "demo_guide": "/DEMO_PRESENTACION.md"
        }
    }


# 🧾 RUTA VENTAS - Página de ventas
@app.get("/ventas", response_class=HTMLResponse)
async def ventas():
    """💸 Devuelve la página de ventas como HTML"""
    return HTMLResponse(content=get_sales_html(), status_code=200)

# 🔌 API ENDPOINTS PARA DATOS JSON - Rutas para intercambiar datos (para programas)

# 📋 OBTENER TODOS LOS PRODUCTOS - GET /api/productos
@app.get(
    "/api/productos",
    response_model=List[Product],
    summary="Obtener todos los productos",
    description="Retorna la lista completa de productos con toda su información incluyendo stock disponible.",
    tags=["Productos"]
)
async def obtener_productos():
    """
    📦 Obtiene todos los productos del inventario
    
    Retorna una lista completa con todos los productos registrados, incluyendo:
    - ID único del producto
    - Nombre y descripción
    - Categoría
    - Precio actual
    - Stock disponible
    - Estado de disponibilidad
    - Fecha de agregado
    """
    return productos_db

# 🔍 OBTENER UN PRODUCTO ESPECÍFICO - GET /api/productos/123
@app.get(
    "/api/productos/{producto_id}",
    response_model=Product,
    summary="Obtener un producto por ID",
    description="Busca y retorna un producto específico usando su identificador único.",
    tags=["Productos"]
)
async def obtener_producto(producto_id: int):
    """
    🎯 Obtiene los detalles de un producto específico
    
    - **producto_id**: ID único del producto a buscar
    
    Retorna toda la información del producto si existe, o un error 404 si no se encuentra.
    """
    producto = next((p for p in productos_db if p.id == producto_id), None)
    
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return producto

# ➕ CREAR NUEVO PRODUCTO - POST /api/productos
@app.post(
    "/api/productos",
    response_model=Product,
    status_code=201,
    summary="Crear un nuevo producto",
    description="Crea un nuevo producto en el inventario con todos sus datos. **Requiere autenticación** (Admin o Vendedor)",
    tags=["Productos"]
)
async def crear_producto(
    producto: ProductCreate,
    current_user: dict = Depends(jwt_middleware.require_admin_or_vendedor)
):
    """
    🆕 Crea un nuevo producto en el inventario
    
    **🔐 ENDPOINT PROTEGIDO** - Requiere autenticación JWT
    - **Roles permitidos**: Admin, Vendedor
    - **Header requerido**: `Authorization: Bearer <access_token>`
    
    Campos requeridos:
    - **nombre**: Nombre del producto (mínimo 1 carácter)
    - **categoria**: Categoría del producto
    - **precio**: Precio del producto (debe ser mayor que 0)
    
    Campos opcionales:
    - **disponible**: Si está disponible para venta (por defecto: true)
    - **stock**: Cantidad en inventario (por defecto: 0)
    - **descripcion**: Descripción detallada del producto
    
    El sistema asignará automáticamente:
    - ID único
    - Fecha de creación
    
    Retorna el producto creado con todos sus datos incluyendo el ID asignado.
    """
    global next_id
    
    nuevo_producto = Product(
        id=next_id,
        **producto.dict(),
        fecha_agregado=datetime.now()
    )
    
    productos_db.append(nuevo_producto)
    next_id += 1
    
    # 💾 Guardar cambios en archivo
    guardar_productos()
    
    return nuevo_producto

@app.put(
    "/api/productos/{producto_id}",
    response_model=Product,
    summary="Actualizar un producto",
    description="Actualiza parcial o totalmente los datos de un producto existente. **Requiere autenticación** (Admin o Vendedor)",
    tags=["Productos"]
)
async def actualizar_producto(
    producto_id: int, 
    producto_update: ProductUpdate,
    current_user: dict = Depends(jwt_middleware.require_admin_or_vendedor)
):
    """
    ✏️ Actualiza un producto existente
    
    **🔐 ENDPOINT PROTEGIDO** - Requiere autenticación JWT
    - **Roles permitidos**: Admin, Vendedor
    - **Header requerido**: `Authorization: Bearer <access_token>`
    
    - **producto_id**: ID del producto a actualizar
    
    Campos actualizables (todos opcionales):
    - **nombre**: Nuevo nombre del producto
    - **categoria**: Nueva categoría
    - **precio**: Nuevo precio
    - **stock**: Nueva cantidad en inventario
    - **disponible**: Nuevo estado de disponibilidad
    - **descripcion**: Nueva descripción
    
    Solo se actualizarán los campos enviados. Los campos no enviados mantendrán su valor actual.
    
    Retorna el producto actualizado con todos sus datos.
    """
    producto_index = next((i for i, p in enumerate(productos_db) if p.id == producto_id), None)
    if producto_index is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto_actual = productos_db[producto_index]
    datos_actualizados = producto_update.dict(exclude_unset=True)
    
    for campo, valor in datos_actualizados.items():
        setattr(producto_actual, campo, valor)
    
    # 🔄 Actualizar disponibilidad automáticamente basada en el stock
    if 'stock' in datos_actualizados:
        if producto_actual.stock > 0:
            producto_actual.disponible = True
        else:
            producto_actual.disponible = False
    
    # 💾 Guardar cambios en archivo
    guardar_productos()
    
    return producto_actual

@app.delete(
    "/api/productos/{producto_id}",
    summary="Eliminar un producto",
    description="Elimina permanentemente un producto del inventario. **Requiere autenticación** (Solo Admin)",
    tags=["Productos"]
)
async def eliminar_producto(
    producto_id: int,
    current_user: dict = Depends(jwt_middleware.require_admin)
):
    """
    🗑️ Elimina un producto del inventario
    
    **🔐 ENDPOINT PROTEGIDO** - Requiere autenticación JWT
    - **Rol permitido**: Solo Admin
    - **Header requerido**: `Authorization: Bearer <access_token>`
    
    - **producto_id**: ID del producto a eliminar
    
    ⚠️ **ADVERTENCIA**: Esta acción es permanente y no se puede deshacer.
    
    Retorna un mensaje confirmando la eliminación exitosa.
    """
    producto_index = next((i for i, p in enumerate(productos_db) if p.id == producto_id), None)
    if producto_index is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto_eliminado = productos_db.pop(producto_index)
    
    # 💾 Guardar cambios en archivo
    guardar_productos()
    
    return {"mensaje": f"Producto '{producto_eliminado.nombre}' eliminado exitosamente"}

# 🛒 ENDPOINT COMPRAR - Realiza una compra y descuenta del inventario
@app.post("/api/compras")
async def realizar_compra(compra: CompraRequest):
    """
    🛒 Realiza una compra de un producto con diferentes modos de procesamiento
    
    - **producto_id**: ID del producto a comprar
    - **cantidad**: Cantidad de unidades a comprar
    - **modo**: Modo de procesamiento (HTTP_DIRECTO, REINTENTOS_SIMPLES, BACKOFF_EXPONENCIAL, REDIS_QUEUE, RABBITMQ)
    
    Descuenta del stock disponible y procesa según el modo seleccionado.
    """
    # � LOG: Registrar qué instancia procesa esta compra
    print(f"🏷️ [INSTANCIA {INSTANCE_ID}] Procesando compra - Producto: {compra.producto_id}, Cantidad: {compra.cantidad}, Modo: {compra.modo}")
    
    # �🚨 VALIDACIÓN DE SERVICIOS ANTES DE PROCESAR LA COMPRA
    def validar_servicios_disponibles(modo):
        network_disabled = not connection_status.get("general_network", True)
        
        if network_disabled:
            return {
                "valido": False, 
                "error": "Red General desactivada",
                "mensaje": "🚨 COMPRA BLOQUEADA: Red General sin conexión. Reactiva la red desde el simulador."
            }
        
        if modo == "HTTP_DIRECTO":
            if not connection_status.get("http_directo", True):
                return {
                    "valido": False,
                    "error": "HTTP Directo desactivado", 
                    "mensaje": "🚨 COMPRA BLOQUEADA: Servicio HTTP Directo desactivado. Reactiva desde el simulador."
                }
        elif modo == "REINTENTOS_SIMPLES":
            if not connection_status.get("reintentos_simples", True):
                return {
                    "valido": False,
                    "error": "Reintentos Simples desactivado",
                    "mensaje": "🚨 COMPRA BLOQUEADA: Servicio Reintentos Simples desactivado. Reactiva desde el simulador."
                }
        elif modo == "BACKOFF_EXPONENCIAL":
            if not connection_status.get("backoff_exponencial", True):
                return {
                    "valido": False,
                    "error": "Backoff Exponencial desactivado",
                    "mensaje": "🚨 COMPRA BLOQUEADA: Servicio Backoff Exponencial desactivado. Reactiva desde el simulador."
                }
        elif modo == "REINTENTOS_SOFISTICADOS":
            if not connection_status.get("reintentos_sofisticados", True):
                return {
                    "valido": False,
                    "error": "Reintentos Sofisticados desactivado",
                    "mensaje": "🚨 COMPRA BLOQUEADA: Servicio Reintentos Sofisticados desactivado. Reactiva desde el simulador."
                }
        elif modo == "REDIS_QUEUE":
            if not connection_status.get("redis", True):
                return {
                    "valido": False,
                    "error": "Redis desactivado",
                    "mensaje": "🚨 COMPRA BLOQUEADA: Servicio Redis desactivado. Reactiva desde el simulador."
                }
        elif modo == "RABBITMQ":
            if not connection_status.get("rabbitmq", True):
                return {
                    "valido": False,
                    "error": "RabbitMQ desactivado",
                    "mensaje": "🚨 COMPRA BLOQUEADA: Servicio RabbitMQ desactivado. Reactiva desde el simulador."
                }
        
        return {"valido": True}
    
    # Validar servicios ANTES de continuar
    validacion = validar_servicios_disponibles(compra.modo)
    if not validacion["valido"]:
        raise HTTPException(
            status_code=503,  # Service Unavailable
            detail={
                "error": validacion["error"],
                "mensaje": validacion["mensaje"],
                "modo_solicitado": compra.modo,
                "estado_servicios": connection_status,
                "tipo_error": "SERVICIO_DESACTIVADO"
            }
        )
    
    # Buscar el producto
    producto = next((p for p in productos_db if p.id == compra.producto_id), None)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Validar que el producto esté disponible
    if not producto.disponible:
        raise HTTPException(status_code=400, detail="Producto no disponible")
    
    # Validar stock suficiente
    if producto.stock < compra.cantidad:
        raise HTTPException(
            status_code=400, 
            detail=f"Stock insuficiente. Solo hay {producto.stock} unidades disponibles"
        )
    
    # Realizar la compra: descontar del stock
    producto.stock -= compra.cantidad
    
    # Si se agota el stock, marcar como no disponible
    if producto.stock == 0:
        producto.disponible = False
    
    # 💾 Guardar cambios en archivo
    guardar_productos()
    
    # Crear mensaje de compra
    mensaje_compra = {
        "timestamp": datetime.now().isoformat(),
        "producto_id": producto.id,
        "producto_nombre": producto.nombre,
        "categoria": producto.categoria,
        "precio_unitario": producto.precio,
        "cantidad_comprada": compra.cantidad,
        "total_pagado": round(producto.precio * compra.cantidad, 2),
        "stock_restante": producto.stock,
        "modo_procesamiento": compra.modo,
        "estado": "completada"
    }
    
    # Respuesta base
    respuesta = {
        "mensaje": f"Compra exitosa de {compra.cantidad} unidad(es) de '{producto.nombre}'",
        "producto_id": producto.id,
        "producto_nombre": producto.nombre,
        "cantidad_comprada": compra.cantidad,
        "stock_restante": producto.stock,
        "total_pagado": round(producto.precio * compra.cantidad, 2),
        "disponible": producto.disponible,
        "modo_procesamiento": compra.modo
    }
    
    # Procesar según el modo seleccionado
    if compra.modo == "RABBITMQ":
        # Enviar mensaje a RabbitMQ
        resultado = enviar_mensaje_compra(mensaje_compra)
        if resultado["success"]:
            respuesta["procesamiento"] = "✅ Venta procesada exitosamente via RabbitMQ"
            respuesta["rabbitmq_status"] = resultado["message"]
            respuesta["cola"] = resultado["queue"]
            respuesta["detalles"] = "Mensaje enviado a cola con garantías de entrega"
        else:
            # Error en RabbitMQ - devolver respuesta de error
            respuesta["procesamiento"] = "❌ ERROR en procesamiento RabbitMQ"
            respuesta["rabbitmq_status"] = resultado["error"]
            respuesta["error_type"] = resultado["error_type"]
            respuesta["detalles"] = resultado["message"]
            respuesta["alerta"] = "🚨 VENTA NO PROCESADA: Problema con RabbitMQ"
            respuesta["estado"] = "fallida"
            
    elif compra.modo == "HTTP_DIRECTO":
        # Verificar estado específico de HTTP DIRECTO
        http_directo_disabled = not connection_status.get("http_directo", True)
        network_disabled = not connection_status.get("general_network", True)
        
        if http_directo_disabled or network_disabled:
            servicio_afectado = "HTTP Directo" if http_directo_disabled else "Red General"
            respuesta["procesamiento"] = f"❌ {servicio_afectado.upper()} NO DISPONIBLE"
            respuesta["detalles"] = f"Servicio {servicio_afectado} desactivado - Sin reintentos en HTTP Directo"
            respuesta["alerta"] = f"🚨 VENTA FALLIDA: {servicio_afectado} sin conexión"
            respuesta["error_type"] = "HTTP_DIRECTO_DISABLED"
            respuesta["recomendacion"] = f"Reactiva '{servicio_afectado}' desde el simulador o usa un modo con reintentos"
            respuesta["estado"] = "fallida"
        # Simular posible fallo en HTTP directo (sin reintentos)
        elif random.random() < 0.15:  # 15% probabilidad de fallo
            respuesta["procesamiento"] = "❌ ERROR en HTTP Directo"
            respuesta["detalles"] = "Fallo en procesamiento directo - Sin reintentos disponibles"
            respuesta["alerta"] = "🚨 VENTA FALLIDA: Error de conexión"
            respuesta["error_type"] = "HTTP_DIRECT_ERROR"
            respuesta["recomendacion"] = "Usa un modo con reintentos o verifica tu conexión"
            respuesta["estado"] = "fallida"
        else:
            respuesta["procesamiento"] = "✅ Procesado directamente via HTTP"
            respuesta["detalles"] = "Procesamiento inmediato exitoso (sin tolerancia a fallos)"
        
    elif compra.modo == "REINTENTOS_SIMPLES":
        resultado = procesar_con_reintentos(mensaje_compra)
        respuesta["procesamiento"] = resultado["mensaje"]
        respuesta["detalles"] = f"Status: {resultado['status']}"
        
        if resultado["status"] == "success":
            respuesta["intento_exitoso"] = resultado["intento"]
            respuesta["resumen"] = resultado["detalles"]
        else:
            respuesta["alerta"] = "🚨 VENTA FALLIDA después de múltiples reintentos"
            respuesta["error_type"] = resultado.get("error_type", "RETRY_FAILED")
            respuesta["errores"] = resultado.get("errores", [])
            respuesta["recomendacion"] = resultado.get("recomendacion", "Intenta más tarde")
            respuesta["estado"] = "fallida"
        
    elif compra.modo == "BACKOFF_EXPONENCIAL":
        resultado = procesar_con_backoff_exponencial(mensaje_compra)
        respuesta["procesamiento"] = resultado["mensaje"]
        respuesta["detalles"] = f"Status: {resultado['status']}"
        
        if resultado["status"] == "success":
            respuesta["intento_exitoso"] = resultado["intento"]
            respuesta["tiempo_total"] = resultado.get("tiempo_total_esperas", "N/A")
            respuesta["resumen"] = resultado.get("detalles", "")
        else:
            respuesta["alerta"] = "🚨 VENTA FALLIDA: Backoff exponencial agotado"
            respuesta["error_type"] = resultado.get("error_type", "BACKOFF_FAILED")
            respuesta["tiempo_total"] = resultado.get("tiempo_total_esperas", "N/A")
            respuesta["errores"] = resultado.get("errores", [])
            respuesta["recomendacion"] = resultado.get("recomendacion", "Sistema con problemas")
            respuesta["estado"] = "fallida"
        
    elif compra.modo == "REINTENTOS_SOFISTICADOS":
        resultado = procesar_con_reintentos_sofisticados(mensaje_compra)
        respuesta["procesamiento"] = resultado["mensaje"]
        respuesta["detalles"] = f"Status: {resultado['status']}"
        
        if resultado["status"] == "success":
            respuesta["intento_exitoso"] = resultado["intento"]
            respuesta["tiempo_total"] = resultado.get("tiempo_total_esperas", "0 segundos")
            respuesta["resumen"] = resultado.get("detalles", "")
            respuesta["modo_especial"] = "🎯 Reintentos Sofisticados (1,2,4,8,16s)"
        else:
            respuesta["alerta"] = "🚨 VENTA FALLIDA: Reintentos Sofisticados agotados"
            respuesta["error_type"] = resultado.get("error_type", "SOFISTICADOS_FAILED")
            respuesta["tiempo_total"] = resultado.get("tiempo_total_esperas", "31 segundos")
            respuesta["errores"] = resultado.get("errores", [])
            respuesta["recomendacion"] = resultado.get("recomendacion", "Sistema sofisticado con problemas")
            respuesta["modo_especial"] = "🎯 Reintentos Sofisticados (5 intentos fallidos)"
            respuesta["estado"] = "fallida"
        
    elif compra.modo == "REDIS_QUEUE":
        resultado = agregar_a_redis_queue(mensaje_compra)
        
        if resultado["success"]:
            respuesta["procesamiento"] = "✅ Enviado a cola Redis exitosamente"
            respuesta["redis_status"] = f"Queue ID: {resultado['queue_id']}, Posición en cola: {resultado['queue_size']}"
            respuesta["detalles"] = resultado["message"]
        else:
            respuesta["procesamiento"] = "❌ ERROR en Redis Queue"
            respuesta["redis_status"] = resultado["error"]
            respuesta["error_type"] = resultado["error_type"]
            respuesta["detalles"] = resultado["message"]
            respuesta["alerta"] = "🚨 VENTA NO PROCESADA: Problema con Redis"
            respuesta["recomendacion"] = resultado["recomendacion"]
            respuesta["estado"] = "fallida"
        
    else:
        respuesta["procesamiento"] = "⚠️ Modo no reconocido, procesado como HTTP directo"
        respuesta["alerta"] = "🟡 ADVERTENCIA: Modo de procesamiento no válido"
    
    return respuesta

# 📦 ENDPOINT REDIS QUEUE - Para consultar estado de la cola
@app.get("/api/redis-queue")
async def obtener_estado_redis_queue():
    """Obtiene el estado de la cola Redis simulada"""
    with redis_lock:
        return {
            "cola_size": len(redis_queue),
            "mensajes_pendientes": len(redis_queue),
            "ultimo_procesado": datetime.now().isoformat() if redis_queue else None,
            "mensajes": [{"id": msg["id"], "timestamp": msg["timestamp"], "producto": msg["producto_nombre"]} for msg in redis_queue[-5:]]  # Últimos 5
        }

@app.post("/api/redis-queue/procesar")
async def procesar_siguiente_redis():
    """Procesa el siguiente mensaje de la cola Redis"""
    resultado = procesar_redis_queue()
    return resultado

# Endpoint para estadísticas del dashboard
@app.get("/api/estadisticas")
async def obtener_estadisticas():
    total_productos = len(productos_db)
    productos_disponibles = len([p for p in productos_db if p.disponible])
    productos_agotados = total_productos - productos_disponibles
    
    categorias = {}
    precio_promedio = 0
    
    if productos_db:
        for producto in productos_db:
            categorias[producto.categoria] = categorias.get(producto.categoria, 0) + 1
        precio_promedio = sum(p.precio for p in productos_db) / len(productos_db)
    
    return {
        "total_productos": total_productos,
        "productos_disponibles": productos_disponibles,
        "productos_agotados": productos_agotados,
        "precio_promedio": round(precio_promedio, 2),
        "categorias": categorias
    }

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 CONFIGURACIÓN DEL SERVIDOR
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Determinar si ejecutar con HTTPS o HTTP
    use_https = os.path.exists("certs/cert.pem") and os.path.exists("certs/key.pem")
    
    if use_https:
        print("\n" + "="*70)
        print("🔒 Iniciando EcoMarket API con HTTPS (TLS/SSL)")
        print("="*70)
        print(f"📍 URL: https://localhost:8443")
        print(f"📄 Documentación: https://localhost:8443/docs")
        print(f"🔐 Certificado: certs/cert.pem")
        print(f"⚠️  Advertencia: Certificado autofirmado (solo desarrollo)")
        print(f"   Los navegadores mostrarán advertencia - es normal")
        print("="*70 + "\n")
        
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8443,  # Puerto estándar HTTPS alternativo
            ssl_keyfile="./certs/key.pem",
            ssl_certfile="./certs/cert.pem",
            reload=True
        )
    else:
        print("\n" + "="*70)
        print("⚠️  Iniciando EcoMarket API en HTTP (sin cifrado)")
        print("="*70)
        print(f"📍 URL: http://localhost:8001")
        print(f"📄 Documentación: http://localhost:8001/docs")
        print(f"")
        print(f"💡 Para habilitar HTTPS:")
        print(f"   1. Ejecuta: python generar_certificados.py")
        print(f"   2. Reinicia el servidor")
        print("="*70 + "\n")
        
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8001,
            reload=True
        )
