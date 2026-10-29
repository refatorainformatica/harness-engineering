# Stack pack — Database & migrations

Cross-cutting pack: applies with any language pack when the project owns a schema. Tools: Flyway, Liquibase, EF Core Migrations, Alembic, Django migrations, Prisma, Knex, golang-migrate, Rails migrations, sqlx.

## Principles

- Schema changes **only** through versioned migrations committed with the code; never edit an applied migration — add a new one.
- Every migration is reviewed as a potential **business-rule change** when it alters data semantics (confirmation per `Governance/permissions.md`).
- Backward compatible by default (expand → migrate → contract): add nullable/defaulted columns, dual-write, backfill in batches, remove old columns in a later release.
- Every migration has a tested rollback (down migration) or an explicit, accepted "forward-only" note in the spec.

## Safety

- Destructive statements (`DROP`, `TRUNCATE`, `DELETE` without `WHERE`, column type narrowing) require `ask` and a backup/restore plan; never run against production from an agent (`deny`).
- Large tables: online/concurrent index creation, batched updates, lock timeouts.
- No production data in fixtures, seeds or tests; seeds only with synthetic data.
- Least-privilege database users: the app user cannot run DDL in production.

## Tests

- Migrations applied from scratch and upgraded from the previous release in CI (containerized database — Testcontainers / docker — in the integration suite, not unit tests).
- Repository/query tests in the integration suite; unit tests mock the repository interface.

## Logging

- Migration runs log version, duration and row counts; never log row contents with PII.

## Structure

- Migrations in the tool's standard folder (e.g. `db/migrations/`, `Migrations/`, `alembic/versions/`) with a sortable, descriptive name (`V2026_09_27_1200__add_order_cancel_reason.sql`).
- Queries parameterized always (S3 in `Governance/security.md`).
