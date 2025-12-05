from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import logging
import re

app = FastAPI(title="Semana4 API")
logger = logging.getLogger("semana4")
logging.basicConfig(level=logging.INFO)

EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")


class UserCreate(BaseModel):
    name: str
    email: str


def _publish_wrapper(user_data: dict) -> None:
    """
    Wrapper que importa el publisher en tiempo de ejecución y captura errores
    para que la API no falle si RabbitMQ/pika no están disponibles.
    """
    try:
        from events import publish_user_created
    except Exception as e:
        logger.error("No se pudo importar publish_user_created: %s", e)
        return

    try:
        ok = publish_user_created(user_data)
        if not ok:
            logger.error("La publicación del evento falló para user_id=%s", user_data.get("user_id"))
        else:
            logger.info("Evento enviado correctamente user_id=%s", user_data.get("user_id"))
    except Exception:
        logger.exception("Error publicando evento en background")


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/users")
async def create_user(user: UserCreate, background_tasks: BackgroundTasks):
    if not EMAIL_RE.fullmatch(user.email):
        raise HTTPException(status_code=422, detail="email inválido")
    new_user = {
        "user_id": "u-" + user.email.split("@")[0],
        "name": user.name,
        "email": user.email,
    }
    background_tasks.add_task(_publish_wrapper, new_user)
    return {"user_id": new_user["user_id"]}