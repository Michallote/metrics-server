# metrics-server

```
project-root/
├── docker-compose.yml
├── .env
├── fastapi-app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
├── grafana/
│   └── provisioning/
│       └── datasources/
│           └── postgres.yaml
└── superset/
    └── superset-init.sh

```

### Prerequisites
| Tool | Minimum version | Purpose |
|------|-----------------|---------|
| **Docker Engine** | 20.10+ | Runs the containers |
| **Docker Compose** | v2 (built-in to recent Docker) | Or `docker compose` CLI plugin |

> Verify:  
> ```bash
> docker --version
> docker compose version
> ```

---

### 1. Clone the project

```bash
git clone gh:metrics-server
# (or git-clone your repo if you committed them there)
```

> **Tip:** keep the `.env` file outside version control if you’ll use real passwords (`echo .env >> .gitignore`).

---

### 2. Adjust environment variables (optional)

Open **`.env`** and change any of:

```dotenv
POSTGRES_USER=appuser
POSTGRES_PASSWORD=secretpassword
POSTGRES_DB=appdb
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=adminpass
SUPERSET_SECRET_KEY=someSuperSecretKey
SUPERSET_ADMIN_USER=admin
SUPERSET_ADMIN_PASSWORD=adminpass
```

---

### 3. Build & start the stack

```bash
docker compose up -d --build
```

* **`--build`** ensures the FastAPI image is constructed on first run.  
* The first start may take a minute while Superset boots and initialises its metadata.

---

### 4. Verify containers

```bash
docker compose ps          # check STATUS → healthy or running
docker compose logs -f     # watch combined logs
```

You should see messages like *“Postgres is ready”* and *“superset init finished”*.

---

### 5. Access the services

| Component | URL | Default login |
|-----------|-----|---------------|
| **FastAPI** | <http://localhost:8000> | *no auth* – interactive docs at `/docs` |
| **Grafana** | <http://localhost:3000> | `admin / adminpass` |
| **Superset** | <http://localhost:8088> | `admin / adminpass` |

---

### 6. Quick test of FastAPI ↔ PostgreSQL

```bash
# create an item
curl -X POST http://localhost:8000/items/ \
     -H "Content-Type: application/json" \
     -d '{"name":"widget","description":"demo record"}'

# fetch items
curl http://localhost:8000/items/
```

The JSON list returned should include the item you just created.

---

### 7. Explore data in Grafana & Superset

* **Grafana:**  
  *Log in → Connections → Data sources → “Postgres” is already present.*  
  Create a panel and run e.g. `SELECT * FROM items`.

* **Superset:**  
  Database *“Postgres”* is pre-registered.  
  Go to **SQL Lab → SQL Editor**, pick the database/schema, and query `items`.

---

### 8. Stopping & removing

```bash
# Stop containers but keep data volumes
docker compose down

# Stop **and** delete volumes (PostgreSQL & Grafana data lost)
docker compose down -v
```

---

That’s it—your minimal LGTM (Loki-Grafana-Tempo-Mimir variant) stack with PostgreSQL, FastAPI and Superset is live and wired together.