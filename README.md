# Grial Backend

API central para validación de suscripciones en un marketplace multi-tenant.

## Stack

- **Framework**: FastAPI (Python async)
- **BD**: PostgreSQL 15
- **Cache**: Redis 7
- **Auth**: Clerk OAuth2/JWT
- **Containerización**: Docker + Docker Compose
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic

## Requisitos

### Local (desarrollo)
- Python 3.11+
- Docker + Docker Compose
- Git

### VPS (producción)
- Docker + Docker Compose
- Git

## Setup Local

### 1. Clonar y entrar al proyecto

```bash
git clone https://github.com/tuusuario/grial-backend.git
cd grial-backend
```

### 2. Crear archivo .env

```bash
cp .env.example .env
```

Luego edita `.env` y llena tus valores reales:
- `CLERK_SECRET_KEY` (de https://dashboard.clerk.com/)
- `DATABASE_URL` (será `postgresql://marketplace_user:marketplace_password@db:5432/marketplace`)
- `REDIS_URL` (será `redis://cache:6379/0`)

**⚠️ NUNCA commites `.env` al repo. Está en `.gitignore`.**

### 3. Ejecutar Docker Compose

```bash
# Inicia los 3 servicios (FastAPI, PostgreSQL, Redis)
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f api

# Cuando quieras parar
docker-compose down
```

### 4. Verificar que funciona

```bash
# Health check
curl http://localhost:8000/health

# Ver documentación automática (Swagger UI)
open http://localhost:8000/docs

# O desde la terminal
curl -X GET http://localhost:8000/
```

### 5. Dentro del container

```bash
# Ejecutar comandos dentro del container FastAPI
docker-compose exec api bash

# Ej: correr tests
docker-compose exec api pytest

# Ej: aplicar migrations (Fase 2)
docker-compose exec api alembic upgrade head
```

## Estructura del proyecto

```
grial-backend/
├── app/                    # Código principal
│   ├── main.py            # Punto de entrada
│   ├── core/              # Config, security, exceptions
│   ├── api/               # Rutas HTTP
│   ├── models/            # ORM + Pydantic schemas
│   ├── services/          # Lógica de negocio
│   ├── database/          # Conexión a PostgreSQL + migrations
│   └── utils/             # Helpers (logging, etc)
├── tests/                 # Tests unitarios
├── docker-compose.yml     # Orquesta 3 servicios
├── Dockerfile             # Imagen de FastAPI
├── requirements.txt       # Dependencias Python
├── .env.example           # Plantilla de variables
└── README.md             # Este archivo
```

## Flujo de desarrollo

### Cambios en código

Como el `docker-compose.yml` monta un volumen con hot reload:
```bash
# En app/main.py cambias algo
# El container detecta el cambio y reinicia automáticamente
# No necesitas hacer docker-compose up nuevamente
```

### Nuevas dependencias

```bash
# 1. Agregate a requirements.txt
# 2. Rebuild la imagen
docker-compose build api

# 3. Reinicia
docker-compose up -d api
```

### Cambios en la BD (schema)

(Implementarás esto en Fase 2 con Alembic)

```bash
# 1. Crear una migration
docker-compose exec api alembic revision --autogenerate -m "Add new column"

# 2. Aplicarla
docker-compose exec api alembic upgrade head

# 3. Commitea los archivos de migration a Git
git add app/database/migrations/versions/
git commit -m "Add new column migration"
```

## Deploy a VPS (Hostinger)

### 1. Instalar Docker en la VPS

```bash
# Conectate a la VPS via SSH
ssh root@tu_ip_vps

# Instala Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instala Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verifica
docker --version
docker-compose --version
```

### 2. Clonar el repo en la VPS

```bash
cd /opt  # o dónde prefieras
sudo git clone https://github.com/tuusuario/grial-backend.git
cd marketplace-backend

# Cambiar permisos si es necesario
sudo chown -R $USER:$USER .
```

### 3. Crear .env con valores reales

```bash
cp .env.example .env
nano .env  # O tu editor favorito

# Llena:
# - CLERK_SECRET_KEY (la real, no test)
# - DATABASE_URL (mismo, no cambia mucho)
# - REDIS_URL (mismo)
```

### 4. Ejecutar

```bash
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Verificar
curl http://localhost:8000/health
```

### 5. Actualizaciones futuras

```bash
# Pullear cambios de GitHub
git pull origin main

# Rebuild imagen si cambiaron dependencias
docker-compose build api

# Reiniciar
docker-compose down
docker-compose up -d
```

## Debugging

### Logs

```bash
# Todos los logs
docker-compose logs

# Solo FastAPI
docker-compose logs -f api

# Solo PostgreSQL
docker-compose logs -f db

# Solo Redis
docker-compose logs -f cache
```

### Entrar a la BD

```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U marketplace_user -d marketplace

# Dentro de psql:
# \dt - ver todas las tablas
# \d subscriptions - ver estructura de tabla
# SELECT * FROM subscriptions LIMIT 5; - ver datos
# \q - salir
```

### Entrar a Redis

```bash
# Conectar a Redis CLI
docker-compose exec cache redis-cli

# Dentro de redis:
# KEYS * - ver todas las claves
# GET mi_clave - obtener valor
# FLUSHDB - borrar todo (cuidado!)
# QUIT - salir
```

## Testing (Fase 2)

```bash
# Ejecutar todos los tests
docker-compose exec api pytest

# Con cobertura
docker-compose exec api pytest --cov=app

# Un archivo específico
docker-compose exec api pytest tests/test_subscriptions.py

# Verbose
docker-compose exec api pytest -v
```

## Linting y Formatting (Fase 2)

```bash
# Formatear código con Black
docker-compose exec api black app/

# Verificar con Flake8
docker-compose exec api flake8 app/

# Type checking con MyPy
docker-compose exec api mypy app/
```

## Fases del proyecto

- **Fase 1** ✅ (ACTUAL): Setup Docker, estructura de carpetas
- **Fase 2**: Base de datos, modelos, migrations, Alembic
- **Fase 3**: Endpoints básicos (`GET /subscriptions/{user_id}`)
- **Fase 4**: Integración Clerk (webhooks, JWT validation)
- **Fase 5**: Redis caching
- **Fase 6**: Tests, documentación, CI/CD
- **Fase 7**: Deployar a VPS

---

**¿Preguntas?** Abre un issue en GitHub.