# Dockerfile
# Define cómo construir la imagen Docker de FastAPI
# Comando: docker build -t marketplace-api:latest .

# ============================================
# STAGE 1: Base image
# ============================================
FROM python:3.11-slim

# Metadatos
LABEL maintainer="tu-email@example.com"
LABEL description="FastAPI backend para marketplace multi-tenant"

# Working directory dentro del container
WORKDIR /app

# ============================================
# Instalaciones del sistema
# ============================================
# RUN (ejecuta comandos durante build)
# -y = yes automático para apt-get
# --no-install-recommends = instala sólo lo esencial (reduce tamaño imagen)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# Dependencias Python
# ============================================
# Copia requirements.txt desde host a container
COPY requirements.txt .

# Instala dependencias Python
# pip install sin cache (ahorra espacio)
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# Código de la aplicación
# ============================================
# Copia TODO el código desde host a /app en el container
COPY . .

# ============================================
# Permisos y usuario no-root (seguridad)
# ============================================
# Crea un usuario sin privilegios (no ejecutar como root en producción)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# ============================================
# Exposición de puertos
# ============================================
# EXPOSE sólo documenta (es docker-compose.yml quien mapea puertos)
EXPOSE 8000

# ============================================
# Health check
# ============================================
# Docker puede verificar que el container está "saludable"
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# ============================================
# Comando por defecto
# ============================================
# Puede ser overrideado por docker-compose (command: ...)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]