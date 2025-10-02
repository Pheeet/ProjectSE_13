## Quick context

This is a small Vue 3 + Vite frontend demo focused on a "research publications" dashboard. The app is single-page (Vue Router) and intentionally uses local component/page state and a small mock data service instead of a global store.

## Big-picture architecture (what matters)
- Framework: Vue 3 (SFCs with <script setup>) + Vite. See `package.json` scripts: `dev`, `build`, `preview`.
- Entrypoint: `src/main.js` mounts the app and imports `@/styles/research.css`.
- Routing: `src/router/index.js` defines two pages: `/research/horizontal` -> `ResearchHorizontal.vue` and `/research/vertical` -> `ResearchVertical.vue`.
- Feature area: `src/features/research/**` contains pages, presentational components, and a simple data service. Pages orchestrate data and UI; components are dumb/presentational.
- Data service: `src/services/search.service.js` returns mocked results via `searchPublications(params)` and `getFacets()`; pages call this and then apply client-side filters.

## Key files to inspect (examples)
- `src/features/research/pages/ResearchVertical.vue` — sidebar + results + preview. Uses `reactive`, `ref`, `onMounted`, and local helper `applyFilters()`.
- `src/features/research/pages/ResearchHorizontal.vue` — dashboard with charts (uses `vue-chartjs` + `chart.js` + `chartjs-plugin-datalabels`). See ChartJS registration pattern.
- `src/features/research/components/SearchBar.vue` — emits `update:modelValue`, `search`, `reset`. Pattern: parent binds `:modelValue` and listens for `update:modelValue`.
- `src/features/research/components/ResultList.vue` and `ResultCard.vue` — simple list/card presentation examples.
- `src/services/search.service.js` — mock API; preserves the shape { items: [...] } and simulates latency.
- `src/styles/*.css` — theme via CSS variables (e.g. `--bg`, `--panel`) — pages rely heavily on these variables.

## Conventions & patterns agents should follow
- SFCs use <script setup>. Use `defineProps()` and `defineEmits()` where appropriate.
- v-model on custom components follows the `modelValue` + `update:modelValue` convention (see `SearchBar.vue`).
- Pages prefer local state (Vue `reactive` / `ref`), call `searchPublications()` and then run an `applyFilters(rows)` helper to implement client-side constraints such as year ranges.
- Services return Promises and the shape `{ items: [...] }`. When replacing the mock service with a real API, keep the same return shape to avoid changes across pages.
- Charts: call `ChartJS.register(...)` once in the component that uses charts (see `ResearchHorizontal.vue`). When adding new chart components, follow the same registration pattern.
- Export helpers and simple utilities live inside page components (e.g. `exportCSV()` in `ResearchHorizontal.vue`). Keep these small and colocated unless they are shared.

## Integration points & change guidance
- To swap the mock service for a real backend, update `src/services/search.service.js` but keep `getFacets()` and `searchPublications(params)` signatures. Return `{ items }` where `items` is an array of publications.
- To add a global store (Pinia/Vuex), note the repo currently has an empty `src/features/research/stores/research.store.js` file — adding a store is safe but pages currently expect local state; update pages to read/write from the store if migrating.
- Router: add routes in `src/router/index.js`. Pages are imported directly (no lazy-loading currently).

## Build / run / debug (how developers start)
Install deps and run the dev server locally (Vite):

```
npm install
npm run dev
```

Open http://localhost:5173 (default Vite port) and use the browser devtools to debug components; code uses modern ES modules.

## Tests & CI
- No tests found in the repository. If you add tests, prefer Jest or Vitest for unit tests of components and small helpers; add scripts to `package.json`.

## Small gotchas discovered
- Several composables are present but empty: `src/composables/useDebounce.js` and `src/composables/useQueryParams.js` — safe places to centralize behaviors seen inline in pages (debounce for input, sync query params to state).
- `src/features/research/stores/research.store.js` is empty — repository currently does not depend on a store.
- Many strings and UI copy are in Thai; keep encoding/locale in mind when editing templates and tests.

## When making PRs, be mindful
- Keep UI components small and presentation-only (pages handle orchestration).
- Preserve the service API shape `{ items: [...] }` when upgrading from mock to real API.
- When adding new top-level dependencies (Chart.js, CSV export helpers), update `package.json` and list in PR description.

---
If any part of this guidance is unclear or you want more examples (e.g. how to wire a real API, add Pinia, or add unit tests for `SearchBar.vue`), tell me which area to expand and I will iterate.
