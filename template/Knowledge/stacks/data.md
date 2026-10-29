# Stack pack — Data & ML (dbt, Spark, notebooks, orchestration)

Complements [standards.md](../standards.md); combine with [python.md](./python.md) and [database.md](./database.md) when applicable.

## Code docs

- dbt: every model, column and test described in `schema.yml` (English), with owner and grain; Spark/Python jobs follow the language pack.
- Notebooks: a header cell with purpose, inputs, outputs and owner; logic that goes to production moves into versioned modules.

## Tests

- dbt: `unique`, `not_null`, `relationships`, `accepted_values` on keys and critical columns; unit tests (`dbt unit tests`) for transformation logic.
- Spark/pandas: pure transformation functions unit-tested with small in-memory frames (`chispa`, `pandas.testing`); no reads from real buckets/warehouses in unit tests.
- Data quality checks (Great Expectations / Soda / dbt tests) as pipeline gates.
- ML: deterministic seeds; tests for feature engineering and for model input/output contracts; evaluation metrics tracked, not asserted on random splits.

## Coverage

- Python/Scala job code ≥ 80% line per package (language pack tooling); dbt models: every model has tests on its primary key and critical columns.

## Logging

- Jobs log run id, dataset/partition, row counts in and out, rejected rows and elapsed time; never sample rows containing PII.

## Security and governance

- PII classified and masked/tokenized before leaving the raw layer; access by role; no production extracts on laptops or in notebooks committed to git (strip outputs: `nbstripout`).
- Credentials through the platform's secret manager / workload identity.

## Structure

- Layers: `raw/staging` → `intermediate` → `marts` (dbt) or `bronze` → `silver` → `gold`; one folder per domain/feature.
- Orchestration (Airflow, Dagster, Prefect) only schedules and wires; logic lives in tested modules.
