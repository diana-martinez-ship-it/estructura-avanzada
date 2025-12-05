import json
import uuid
import time
from datetime import datetime
import pika

RABBIT_HOST = "localhost"
RABBIT_USER = "user"
RABBIT_PASS = "pass"
EXCHANGE = "user_events"
EXCHANGE_TYPE = "fanout"

def _connection_params():
    return pika.ConnectionParameters(
        host=RABBIT_HOST,
        port=5672,
        credentials=pika.PlainCredentials(RABBIT_USER, RABBIT_PASS),
        heartbeat=60,
        blocked_connection_timeout=30,
    )

def publish_user_created(user_data: dict, max_retries: int = 3) -> bool:
    message = {
        **user_data,
        "event_type": "UsuarioCreado",
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    body = json.dumps(message)
    for attempt in range(1, max_retries + 1):
        conn = None
        try:
            conn = pika.BlockingConnection(_connection_params())
            ch = conn.channel()
            ch.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE, durable=True)
            ch.confirm_delivery()
            ch.basic_publish(
                exchange=EXCHANGE,
                routing_key="",
                body=body,
                properties=pika.BasicProperties(content_type="application/json", delivery_mode=2),
                mandatory=False,
            )
            conn.close()
            print(f"✅ Evento publicado: {message['event_id']}")
            return True
        except Exception as e:
            print(f"❌ publish intento {attempt} error: {e}")
            try:
                if conn and not conn.is_closed:
                    conn.close()
            except Exception:
                pass
            if attempt < max_retries:
                time.sleep(2 ** (attempt - 1))
    return False