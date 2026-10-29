# Stack packs

Language/framework-**specific** rules. The [standards.md](../standards.md) baseline applies to any stack; a pack only **adds** format and tooling — it never contradicts the baseline.

Packs **compose**: language base + framework/platform layer.

| Pack | Base | When (automatic detection) |
|------|------|----------------------------|
| [dotnet.md](./dotnet.md) | — | C# / .NET (`*.sln`, `*.slnx`, `*.csproj`) |
| [blazor.md](./blazor.md) | dotnet | Blazor (`*.razor`, `Microsoft.AspNetCore.Components*`) |
| [java.md](./java.md) | — | Java / Kotlin — Spring, Quarkus, Jakarta (`pom.xml`, `build.gradle*`) |
| [typescript.md](./typescript.md) | — | JavaScript / TypeScript (`package.json`, `tsconfig.json`) |
| [node.md](./node.md) | typescript | Node backend — Express, Fastify, NestJS, Koa |
| [angular.md](./angular.md) | typescript | Angular (`angular.json`, `@angular/core`) |
| [react.md](./react.md) | typescript | React / Next.js (`react` in the dependencies) |
| [flutter.md](./flutter.md) | — | Flutter / Dart (`pubspec.yaml`) |
| [python.md](./python.md) | — | Python — Django, FastAPI, Flask (`pyproject.toml`, `requirements.txt`, `setup.py`) |
| [go.md](./go.md) | — | Go (`go.mod`) |
| [rust.md](./rust.md) | — | Rust (`Cargo.toml`) |
| [php.md](./php.md) | — | PHP — Laravel, Symfony (`composer.json`) |
| [ruby.md](./ruby.md) | — | Ruby — Rails (`Gemfile`) |
| [vue.md](./vue.md) | typescript | Vue / Nuxt (`vue` / `nuxt` in the dependencies) |
| [react-native.md](./react-native.md) | react | React Native / Expo (`react-native` / `expo` in the dependencies) |
| [android.md](./android.md) | java | Android (`AndroidManifest.xml`, `com.android.application` / `com.android.library`) |
| [ios.md](./ios.md) | — | iOS / Swift (`*.xcodeproj`, `*.xcworkspace`, `Package.swift`, `Podfile`) |
| [database.md](./database.md) | — (cross-cutting) | Schema migrations (Flyway, Liquibase, EF Migrations, Alembic, Django, Prisma, Rails, Knex, golang-migrate) |
| [data.md](./data.md) | — (cross-cutting) | Data & ML (`dbt_project.yml`, notebooks, Spark, Airflow/Dagster/Prefect) |
| [devops.md](./devops.md) | — | Containers, Kubernetes/Helm, Terraform/OpenTofu, CI/CD, OpenTelemetry (`Dockerfile`, `*.tf`, `Chart.yaml`, pipelines) |
| [aws.md](./aws.md) | devops | AWS (`provider "aws"`, CDK, SAM/`template.yaml`, `buildspec.yml`, AWS SDK) |
| [azure.md](./azure.md) | devops | Azure (`provider "azurerm"`, `*.bicep`, `azure-pipelines.yml`, `azure.yaml`, Azure SDK) |
| [gcp.md](./gcp.md) | devops | Google Cloud (`provider "google"`, `cloudbuild.yaml`, `app.yaml`, Google Cloud SDK) |
| [oci.md](./oci.md) | devops | Oracle Cloud (`provider "oci"`, OCI SDK) |

## Usage

- Active packs recorded in [Agents/project.md](../../Agents/project.md) (`fill-harness.py` / `enrich-harness.py` detect them).
- The agent reads **only** the active packs (base + layer) — the others stay out of the context.
- Monorepo / multicloud: one pack per part of the stack (e.g. `dotnet` + `blazor` + `angular` + `typescript` + `devops` + `azure`), each applying to the files of its area.
- Stack without a pack (e.g. Elixir, Scala, C/C++, Delphi): copy the closest pack as a model and fill in the same sections.
- Packs that do not apply can be deleted from the project.

## Sections of every pack

1. Code docs — native format of summary + remarks
2. Tests — frameworks, location, naming, determinism
3. Logging — structured API, no interpolation
4. Attributes / annotations / decorators to preserve
5. Structure — where the feature lives and how orchestrators stay lean
6. Coverage — tool and report format for the ≥ 80% gate
