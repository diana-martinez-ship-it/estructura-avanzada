import pika

try:
    # Configuración de conexión
    connection_params = pika.ConnectionParameters(
        host='localhost',
        port=5672,  # Puerto estándar de RabbitMQ (alineado con docker-compose.yml)
        credentials=pika.PlainCredentials('user', 'pass'),
        heartbeat=600,  # Mantiene la conexión viva
        blocked_connection_timeout=300
    )

    # Conectar a RabbitMQ
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    # Declarar la cola
    channel.queue_declare(queue='test_queue', durable=True)

    # Publicar un mensaje
    message = '¡Hola RabbitMQ!'
    channel.basic_publish(
        exchange='',
        routing_key='test_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2  # Hace que el mensaje sea persistente
        )
    )

    print("Mensaje enviado correctamente:", message)

except pika.exceptions.AMQPConnectionError as e:
    print("Error de conexión a RabbitMQ:", e)
except Exception as e:
    print("Ocurrió un error:", e)
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()
        print("Conexión cerrada")
