# dbt_pipeline

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

Current layout, with pieces still to be built marked `(planned)`:

```
dbt_pipeline/
├── src/
│   └── dbt_pipeline/
│       ├── __init__.py
│       ├── ingestion/                 # (planned) client.py, extract.py
│       └── io/                        # (planned) databricks_loader.py
│
├── dagster_project/                   # (planned) assets, definitions, resources
│
├── dbt_project/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   ├── tests/                         # (planned) custom singular dbt tests
│   ├── dbt_project.yml
│   └── profiles.yml                   # dbt-databricks connection config (gitignored)
│
├── tests/
│   └── databricks_connection.py       # manual connection smoke test
│
├── .github/                           # (planned) workflows/ci.yml — lint, pytest, scheduled dbt build
│
├── databricks.yml                     # Databricks Asset Bundle config
├── pyproject.toml
├── uv.lock
├── .env                               # local secrets (gitignored, not committed)
├── .gitignore
└── README.md
```

## Setup

### 1. Clone and install dependencies
```bash
git clone https://github.com/floresql/data_engineering_projects.git dbt_pipeline
cd dbt_pipeline
uv sync
```

### 2. Databricks
- Sign up for [Databricks Free Edition](https://www.databricks.com/learn/free-edition).
- Create a Unity Catalog catalog with `staging`/`marts` schemas (see `dbt_project/dbt_project.yml` for expected schema names).
- Create a small serverless SQL Warehouse and note its **Server hostname** and **HTTP path**.
- Generate a Personal Access Token (Settings → Developer → Access Tokens) with SQL warehouse access.

### 3. Environment variables

Two separate things need the token — they're not interchangeable:

**a) For `tests/databricks_connection.py`** (loaded via `python-dotenv`), create a `.env` file in the project root (gitignored, never commit this):
```bash
DATABRICKS_HOST=dbc-xxxxxxxx-xxxx.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxxxxxxxxxx
DATABRICKS_TOKEN=dapiXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**b) For dbt itself**, `dbt_project/profiles.yml` reads the token via `{{ env_var('DBT_DATABRICKS_TOKEN') }}`. dbt does not read `.env` files, so this must be a real OS environment variable — set it in your shell profile (or as a persistent env var on Windows), not just in `.env`:
```bash
export DBT_DATABRICKS_TOKEN=dapiXXXXXXXXXXXXXXXXXXXXXXXXXXXX
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
