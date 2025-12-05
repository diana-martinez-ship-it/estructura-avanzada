# Semana 1 — Introducción y puesta en marcha

Este documento recoge los objetivos, actividades, recursos y entregables sugeridos para la Semana 1 del curso/proyecto. Está pensado como plantilla editable; modifícalo según las instrucciones del profesor o del equipo.

## Resumen

Objetivo de la semana: familiarizarse con el proyecto, entender la arquitectura general, preparar el entorno de desarrollo y completar las primeras tareas de integración.

## Objetivos específicos

- Clonar el repositorio y ejecutar la aplicación mínima localmente.
- Comprender la estructura de carpetas y los componentes principales.
- Configurar dependencias y entorno (virtualenv / venv / Docker según corresponda).
- Ejecutar al menos un test básico (si existen tests automatizados).

## Requisitos previos

- Git instalado.
- Python 3.8+ (o la versión indicada en el repositorio).
- Docker (opcional, si el proyecto usa contenedores).

## Configuración del entorno (pasos rápidos)

1. Clonar el repositorio:

   git clone <url-del-repo>
   cd <repo>

2. Crear entorno virtual e instalar dependencias (ejemplo con venv):

   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

3. Ejecutar la aplicación mínima (si hay un `main.py` o `app`):

   python main.py

   Ajusta el comando según el punto de entrada del proyecto (por ejemplo `app.py`, `demo_simple.py`, etc.).

4. Ejecutar tests básicos (si hay):

   pytest -q

## Estructura del repositorio (alto nivel)

- `semana_1/` — materiales de la semana 1 (este README).
- `semana7_ia/`, `web/`, `docker-rabbitmq-project/`, etc. — otras carpetas con ejercicios y recursos (ver índice del repo).
- Archivos relevantes: `requirements.txt`, `main.py`, `README.md` principal.

> Nota: revisa el `README.md` raíz para instrucciones del proyecto que sean generales o específicas de despliegue.

## Actividades sugeridas

1. Revisar el `README.md` principal y los documentos `INDICE.md`, `QUICK-START.md`.
2. Identificar el punto de entrada de la aplicación y arrancarlo.
3. Ejecutar las pruebas automatizadas existentes (`test_api.py`, `test_load_balancer.py`, etc.) y anotar fallos.
4. Documentar en este README cualquier paso adicional requerido para reproducir el entorno en tu máquina.

## Entregables de la semana

- Evidencia de ejecución local (captura de pantalla o salida de consola).
- Lista de problemas encontrados y cómo reproducirlos.
- (Opcional) Pull request con mejoras menores de documentación o scripts de inicio.

## Recursos y referencias

- `requirements.txt` — dependencias del proyecto.
- `README.md` raíz — información global del proyecto.
- Carpeta `semana7_ia/` — ejemplo de estructura de ejercicios por semana.

## Checklist

- [ ] Repositorio clonado
- [ ] Entorno creado e instalado
- [ ] Aplicación mínima ejecutada
- [ ] Tests ejecutados
- [ ] Evidencias y notas subidas (o añadidas al README)

## Notas del equipo

Agrega aquí riesgos, preguntas para el instructor o decisiones tomadas durante la semana.

---

Si quieres, adapto este README con pasos específicos del proyecto (por ejemplo, comandos Docker Compose, variables de entorno necesarias, o las rutas de los scripts de ejemplo). Dime qué prefieres y lo ajusto.
