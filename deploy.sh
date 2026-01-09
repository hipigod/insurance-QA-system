#!/bin/bash
set -e

info() { echo "[INFO] $1"; }
warn() { echo "[WARN] $1"; }
err() { echo "[ERROR] $1"; }

if ! command -v docker >/dev/null 2>&1; then
  err "Docker is not installed"
  exit 1
fi

if ! command -v docker compose >/dev/null 2>&1; then
  err "Docker Compose is not available"
  exit 1
fi

if [ ! -f .env ]; then
  warn ".env not found, copying from .env.example"
  cp .env.example .env
  warn "Update MODEL_API_KEY in .env"
fi

mkdir -p backend/data

info "Building images"
docker compose build --no-cache

info "Starting services"
docker compose up -d

info "Waiting for backend health"
for i in {1..30}; do
  if docker compose exec -T backend curl -fsS http://localhost:8000/api/v1/health >/dev/null 2>&1; then
    info "Backend is healthy"
    break
  fi
  sleep 2
  echo -n "."
  if [ "$i" -eq 30 ]; then
    warn "Backend health check timed out"
  fi
done

info "Frontend: http://localhost"
info "Backend health: http://localhost:8000/api/v1/health"
