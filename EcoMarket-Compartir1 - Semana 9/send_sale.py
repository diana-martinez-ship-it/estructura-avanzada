#!/usr/bin/env python
"""
Script para enviar notificaciones de ventas a RabbitMQ
"""
import pika
import json
from datetime import datetime
import sys

RABBIT_HOST = 'localhost'
RABBIT_PORT = 5672
RABBIT_USER = 'user'
RABBIT_PASS = 'pass'
QUEUE_NAME = 'sale_notifications'


def send_sale_notification(sale_data):
    """Envía una notificación de venta a RabbitMQ"""
    try:
        # Configurar credenciales y parámetros de conexión
        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
        params = pika.ConnectionParameters(
            host=RABBIT_HOST,
            port=RABBIT_PORT,
            credentials=credentials,
            heartbeat=600
        )

        # Conectar a RabbitMQ
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # Declarar la cola (durable para persistencia)
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        # Agregar timestamp si no existe
        if 'timestamp' not in sale_data:
            sale_data['timestamp'] = datetime.now().isoformat()

        # Publicar mensaje
        message = json.dumps(sale_data)
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Mensaje persistente
                content_type='application/json'
            )
        )

        print(f"✅ Venta enviada exitosamente: {sale_data}")
        connection.close()
        return True

    except pika.exceptions.AMQPConnectionError as e:
        print(f"❌ Error de conexión a RabbitMQ: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


if __name__ == "__main__":
    # Ejemplo de uso
    sale_example = {
        "sale_id": "SALE-001",
        "product_name": "Manzana Orgánica",
        "quantity": 5,
        "total": 12.50,
        "customer": "Cliente Demo"
    }

    # Si se pasan argumentos, crear venta personalizada
    if len(sys.argv) > 1:
        sale_example["product_name"] = sys.argv[1]
    if len(sys.argv) > 2:
        sale_example["quantity"] = int(sys.argv[2])
    if len(sys.argv) > 3:
        sale_example["total"] = float(sys.argv[3])

    send_sale_notification(sale_example)
