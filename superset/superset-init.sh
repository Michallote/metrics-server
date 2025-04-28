#!/bin/bash
set -e

# initialise Superset metadata & create admin user ONCE
superset db upgrade

superset fab create-admin \
  --username "$SUPERSET_ADMIN_USER" \
  --firstname Superset \
  --lastname Admin \
  --email admin@example.com \
  --password "$SUPERSET_ADMIN_PASSWORD" || true

superset init
