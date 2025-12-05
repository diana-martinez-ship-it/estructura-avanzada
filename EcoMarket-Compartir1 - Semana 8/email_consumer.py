import json
import pika
import time

RABBIT_HOST = "localhost"
RABBIT_USER = "user"
RABBIT_PASS = "pass"
EXCHANGE = "user_events"
EMAIL_QUEUE = "email_queue"

def _params():
    return pika.ConnectionParameters(host=RABBIT_HOST, port=5672,
                                     credentials=pika.PlainCredentials(RABBIT_USER, RABBIT_PASS),
                                     heartbeat=60, blocked_connection_timeout=30)

def process(ch, method, props, body):
    try:
        msg = json.loads(body)
        if msg.get("event_type") == "UsuarioCreado":
            print(f"📧 Enviando email a {msg.get('email')}")
            time.sleep(0.2)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as e:
        print("Error procesando mensaje:", e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    conn = pika.BlockingConnection(_params())
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type='fanout', durable=True)
    ch.queue_declare(queue=EMAIL_QUEUE, durable=True, exclusive=False)
    ch.queue_bind(exchange=EXCHANGE, queue=EMAIL_QUEUE)
    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(queue=EMAIL_QUEUE, on_message_callback=process)
    print("🎧 Email consumer esperando...")
    ch.start_consuming()

if __name__ == "__main__":
    main()