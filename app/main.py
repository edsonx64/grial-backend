# app/main.py
# Punto de entrada de FastAPI
# Comando: uvicorn app.main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Carga variables de .env
load_dotenv()

# ============================================
# Crear app FastAPI
# ============================================
app = FastAPI(
    title="Marketplace Backend",
    description="API central para validación de suscripciones multi-tenant",
    version="0.1.0",
)

# ============================================
# CORS Middleware
# ============================================
# Permite que apps satélites hagan requests desde otros dominios
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Rutas básicas (para verificar que funciona)
# ============================================

@app.get("/health")
async def health():
    """
    Endpoint de healthcheck.
    Apps satélites y orquestadores (Kubernetes, Docker, etc) usan esto
    para verificar que el backend está vivo.
    """
    return {
        "status": "healthy",
        "service": "marketplace-api",
        "version": "0.1.0",
    }


@app.get("/ready")
async def readiness():
    """
    Endpoint de readiness.
    Similar a /health, pero verifica que la BD está conectada.
    Implementarás esto en Fase 2 (cuando tengas DB setup).
    """
    # Por ahora, simplemente devolvemos OK
    # En Fase 2: verificarás que PostgreSQL está accesible
    return {
        "status": "ready",
        "database": "connected",  # TODO: verificar conexión real
    }


@app.get("/")
async def root():
    """Root endpoint. Devuelve info sobre la API."""
    return {
        "message": "Welcome to Marketplace Backend",
        "docs": "/docs",  # Swagger UI automático de FastAPI
        "openapi": "/openapi.json",
    }


# ============================================
# Startup / Shutdown events (Fase 2)
# ============================================
# Aquí inicializarás conexiones a BD, Redis, Clerk, etc.
# Por ahora, vacío.

@app.on_event("startup")
async def startup_event():
    """
    Se ejecuta cuando la app inicia.
    - Conectar a PostgreSQL
    - Conectar a Redis
    - Validar Clerk keys
    """
    print("🚀 Iniciando Marketplace Backend...")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Se ejecuta cuando la app se apaga.
    - Cerrar conexiones a BD
    - Limpiar Redis
    """
    print("🛑 Apagando Marketplace Backend...")


# ============================================
# Root context (para debugging)
# ============================================
if __name__ == "__main__":
    # Si ejecutas `python app/main.py` directamente
    # (en desarrollo; en producción usa uvicorn)
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )