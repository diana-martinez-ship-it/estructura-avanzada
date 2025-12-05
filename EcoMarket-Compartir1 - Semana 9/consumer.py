import pika
import json

RABBIT_HOST = 'localhost'
RABBIT_PORT = 5672  # Puerto estándar de RabbitMQ (alineado con docker-compose.yml)
RABBIT_USER = 'user'
RABBIT_PASS = 'pass'
QUEUE_NAME = 'sale_notifications'

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
params = pika.ConnectionParameters(
    host=RABBIT_HOST,
    port=RABBIT_PORT,
    credentials=credentials,
    heartbeat=600
)

try:
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
except Exception as e:
    print("❌ Error de conexión a RabbitMQ:", e)
    exit(1)

def callback(ch, method, properties, body):
    sale = json.loads(body)
    print("Venta recibida:", sale)

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
print("Esperando mensajes...")
channel.start_consuming()
