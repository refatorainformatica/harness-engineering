# Stack pack — Node.js (backend)

Layer on top of [typescript.md](./typescript.md) (read both). Frameworks: Express, Fastify, NestJS, Koa.

## Tests

- Unit: Vitest/Jest (or `node:test`) with repositories, external HTTP, queues and clock mocked.
- Routes/controllers: supertest / `fastify.inject` / `Test.createTestingModule` (Nest) with mocked dependencies — no real database in unit tests.

## Coverage

- As in `typescript.md`; each service/package ≥ 80% lines.

## Logging

- pino / winston / Nest `Logger` with a context object: `logger.info({ orderId, elapsedMs }, 'Order processed')`.
- Correlation id propagated per request; exception in the `err` field.

## Decorators (NestJS / ORMs)

- Preserve `@Module`, `@Controller`, `@Injectable`, `@Get`, `@Body`, `@Entity`, `@Column`, `@IsString`, …

## Structure

- Feature: `src/features/<id>/` (NestJS: `src/<feature>/` with `<feature>.module.ts`) — controller/handler only orchestrates; private helpers become feature services registered in the module.
