@echo off
setlocal

where docker >nul 2>&1
if %errorlevel% neq 0 (
  echo [ERROR] Docker is not installed
  exit /b 1
)

where docker >nul 2>&1
if %errorlevel% neq 0 (
  echo [ERROR] Docker Compose is not available
  exit /b 1
)

if not exist .env (
  echo [WARN] .env not found, copying from .env.example
  copy .env.example .env >nul
  echo [WARN] Update MODEL_API_KEY in .env
)

if not exist backend\data (
  mkdir backend\data
)

echo [INFO] Building images
docker compose build --no-cache

echo [INFO] Starting services
docker compose up -d

echo [INFO] Backend health: http://localhost:8000/api/v1/health
endlocal
