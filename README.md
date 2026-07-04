# dbt_pipeline1

A portfolio data engineering pipeline demonstrating ingestion, transformation, and orchestration using a modern, open-source-friendly stack.

## Architecture

```
Python ingestion (requests/pandas)
        │
        ▼
Databricks Unity Catalog (Delta tables)
        │
        ▼
dbt-databricks (staging → intermediate → marts)
        │
        ▼
Dagster (orchestrates ingestion + dbt as one asset graph)
        │
        ▼
GitHub Actions (lint, test, scheduled dbt build) + dbt docs on GitHub Pages
```

## Tech stack

| Layer | Tool |
|---|---|
| Language / packaging | Python (src layout), uv |
| Ingestion | requests, pandas |
| Warehouse | Databricks (Unity Catalog, Delta Lake, SQL Warehouse) |
| Transformation | dbt-databricks |
| Orchestration | Dagster (dagster-dbt) |
| Testing | pytest, dbt tests |
| CI/CD | GitHub Actions |
| Docs | dbt docs → GitHub Pages |

## Project structure

```
dbt_pipeline1/
├── src/
│   └── my_pipeline/
│       ├── __init__.py
│       ├── ingestion/
│       │   ├── __init__.py
│       │   ├── client.py              # requests session wrapper w/ retries
│       │   └── extract.py             # source-specific pull logic
│       ├── io/
│       │   └── databricks_loader.py   # writes DataFrames to Unity Catalog tables
│       └── utils/
│           └── logging.py
│
├── dagster_project/
│   ├── __init__.py
│   ├── assets/
│   │   ├── ingestion_assets.py        # Dagster assets wrapping ingestion functions
│   │   └── dbt_assets.py              # auto-generated assets from dbt manifest.json
│   ├── definitions.py                 # Definitions object, schedules/sensors
│   └── resources.py                   # Databricks SQL + dbt CLI resources
│
├── dbt_project/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   ├── tests/                         # custom singular dbt tests
│   ├── dbt_project.yml
│   └── profiles.yml                   # dbt-databricks connection config
│
├── tests/
│   ├── test_ingestion.py              # pytest for the ingestion layer
│   └── databricks_connection.py       # manual connection smoke test
│
├── .github/
│   └── workflows/
│       └── ci.yml                     # lint, pytest, scheduled dbt build
│
├── pyproject.toml
├── uv.lock
├── .env                               # local secrets (gitignored, not committed)
├── .gitignore
└── README.md
```

## Setup

### 1. Clone and install dependencies
```bash
git clone https://github.com/<your-username>/dbt_pipeline1.git
cd dbt_pipeline1
uv sync
```

### 2. Databricks
- Sign up for [Databricks Free Edition](https://www.databricks.com/learn/free-edition).
- Create a Unity Catalog catalog `portfolio` with schemas `raw`, `staging`, `marts`.
- Create a small serverless SQL Warehouse and note its **Server hostname** and **HTTP path**.
- Generate a Personal Access Token (Settings → Developer → Access Tokens).

### 3. Environment variables
Create a `.env` file in the project root (never commit this):
```bash
DATABRICKS_HOST=dbc-xxxxxxxx-xxxx.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxxxxxxxxxx
DATABRICKS_TOKEN=dapiXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 4. Verify the connection
```bash
uv run python tests/databricks_connection.py
```

### 5. Run dbt
```bash
cd dbt_project
uv run dbt debug
uv run dbt build
```

### 6. Run Dagster locally
```bash
uv run dagster dev
```
Open the Dagster UI to view and materialize the full ingestion → dbt asset graph.

## CI/CD notes

Because Databricks Free Edition has fair-use compute limits, `dbt build` against the live warehouse runs on a schedule / manual trigger rather than on every push. Lint and unit tests run on every commit.

## License

MIT
