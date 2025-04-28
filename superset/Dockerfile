FROM apache/superset:latest as builder

USER root

# Install dependencies for Superset envsubst
RUN apt-get update && apt-get install -y gettext-base

COPY superset-init.sh /app/superset-init.sh
COPY create_roles.py /app/create_roles.py
COPY superset-load-data.sh /app/superset-load-data.sh
COPY preloaded_connections/ /app/preloaded_connections/
COPY preloaded_dashboards/ /app/preloaded_dashboards/
RUN chmod +x /app/superset-init.sh /app/superset-load-data.sh

# --- Stage 2: Final image ---
FROM apache/superset:latest

COPY --from=builder /app/superset-init.sh /app/superset-init.sh
COPY --from=builder /app/superset-load-data.sh /app/superset-load-data.sh
COPY --from=builder /app/preloaded_connections/ /app/preloaded_connections/
COPY --from=builder /app/preloaded_dashboards/ /app/preloaded_dashboards/

USER superset

ENTRYPOINT ["/bin/bash", "-c", "/app/superset-init.sh && /usr/bin/run-server.sh"]
