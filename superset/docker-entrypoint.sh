#!/bin/bash
set -e
/app/superset-init.sh
exec /usr/bin/run-server.sh
