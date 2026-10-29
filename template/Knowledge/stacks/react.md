# Stack pack — React (includes Next.js)

Layer on top of [typescript.md](./typescript.md) (read both).

## Code docs

- TSDoc on the component and on the props type (each prop with a summary; remarks when there is a usage rule); custom hooks documented as functions.

## Tests

- Vitest/Jest + React Testing Library + `user-event`; `{Component}.test.tsx` in the feature folder.
- Test visible behavior (roles, text), not implementation details; HTTP with MSW; fake timers instead of waits.

## Coverage

- As in `typescript.md`; components and hooks count as testable artifacts (≥ 80% lines).

## Logging

- The application's logger/telemetry with structured context — no `console.log` in production; no template literal in the message.

## Annotations to preserve

- `'use client'` / `'use server'` directives, `export const metadata`/`dynamic`/`revalidate` (Next.js) and decorators when present.

## Structure

- Feature: `src/features/<id>/` (components, hooks, api, types) — routes (`app/`, `pages/`) only compose features.
- Lean components: effects, HTTP calls and rules in the feature's hooks/services.
