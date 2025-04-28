#!/bin/bash
set -e

echo "Loading starter database connection..."

superset db upgrade

# Substitute environment variables into YAML
echo "Substituting environment variables into database connection YAML..."
envsubst < /app/preloaded_connections/postgres_connection.yaml.template > /app/preloaded_connections/postgres_connection.yaml

# Import datasources and dashboards
superset import-datasources -p /app/preloaded_connections/ || true
superset import-dashboards -p /app/preloaded_dashboards/ || true


# Run custom Python for roles/users
echo "Creating roles and users..."
superset shell <<EOF
from create_roles import create_roles_and_users
create_roles_and_users()
EOF

echo "Starter data loaded successfully."
