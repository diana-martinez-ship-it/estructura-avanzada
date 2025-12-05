# 🐍 Imagen base de Python 3.11
FROM python:3.11-slim

# 📁 Establecer directorio de trabajo
WORKDIR /app

# 📋 Copiar archivo de dependencias
COPY requirements.txt .

# 📦 Instalar dependencias (sin caché para reducir tamaño)
RUN pip install --no-cache-dir -r requirements.txt

# 📂 Copiar todo el código de la aplicación
COPY . .

# 🌐 Exponer puerto 8000
EXPOSE 8000

# 🚀 Comando para iniciar la aplicación con logs visibles
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
