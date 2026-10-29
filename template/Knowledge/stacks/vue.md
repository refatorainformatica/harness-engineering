# Stack pack — Vue (incl. Nuxt)

Layer on top of [typescript.md](./typescript.md) (read both).

## Code docs

- TSDoc on composables, stores and components (`defineProps`/`defineEmits` types: every prop and event with a summary; remarks when there is a usage rule).

## Tests

- Vitest + Vue Test Utils (+ Testing Library for Vue); `{Component}.spec.ts` in the feature folder.
- Test visible behavior; HTTP with MSW; Pinia with `createTestingPinia`; fake timers instead of waits.

## Coverage

- `vitest run --coverage` with `lcov` + `cobertura`; `thresholds.lines: 80` per app/package.

## Logging

- Application logger/telemetry with structured context — no `console.log` in production code; no template literals in the message.

## Declarations to preserve

- `<script setup>` macros (`defineProps`, `defineEmits`, `defineModel`, `defineExpose`), `definePageMeta`/`defineNuxtRouteMiddleware` (Nuxt), and decorators when used.

## Structure

- Feature: `src/features/<id>/` (components, composables, stores, api, types) — pages/routes only compose features.
- Lean components: effects, HTTP calls and rules in composables/services of the feature.
