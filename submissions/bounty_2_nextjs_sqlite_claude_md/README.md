# CLAUDE.md — Next.js 15 (App Router) + SQLite (`better-sqlite3` / Turso) SaaS Architecture

## 1. Stack & Pinned Versions
- **Framework**: Next.js `15.1.x` (App Router exclusively; Pages Router `pages/` is strictly forbidden).
- **Runtime**: Node.js `22 LTS` (Server Actions & Route Handlers run on `nodejs` runtime, never `edge`, because `better-sqlite3` requires native C++ bindings).
- **Database**: SQLite in `WAL` mode (`PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON; PRAGMA busy_timeout = 5000;`) via `better-sqlite3` `11.x` locally and `@libsql/client` (Turso) in production.
- **ORM & Migrations**: Drizzle ORM (`drizzle-orm` `0.38.x` + `drizzle-kit` `0.30.x`).
- **Validation**: `zod` `3.24.x` at every Server Action and Route Handler boundary.

## 2. Folder Structure & Naming Conventions
```text
src/
├── app/                      # Next.js 15 App Router routes (kebab-case folders)
│   ├── (marketing)/          # Public landing & pricing pages
│   ├── (dashboard)/          # Authenticated tenant routes
│   └── api/webhooks/         # Stripe / x402 webhook Route Handlers ONLY
├── components/
│   ├── ui/                   # Stateless primitives (PascalCase: Button.tsx)
│   └── features/             # Domain components (PascalCase: BillingTable.tsx)
├── db/
│   ├── index.ts              # Singleton WAL connection + PRAGMA initialization
│   ├── schema.ts             # Single source of truth Drizzle schema (snake_case columns)
│   └── migrations/           # Immutable numbered SQL migrations (0001_init.sql)
└── server/
    ├── actions/              # Mutating Server Actions (*.actions.ts)
    └── queries/              # Read-only DAL functions wrapped in server-only (*.queries.ts)
```

## 3. SQL & Migration Conventions
- **Primary Keys**: Text ULIDs (`id TEXT PRIMARY KEY NOT NULL`) — sortable chronologically and safe across SQLite shards.
- **Timestamps**: Integer Unix milliseconds (`created_at INTEGER NOT NULL`) — avoids SQLite string timezone parsing bugs.
- **Monetary Amounts**: Integer cents/micro-units (`amount_cents INTEGER NOT NULL`) — NEVER use `REAL`/`FLOAT` for currency.
- **Migrations**: Generate via `pnpm db:generate` (`drizzle-kit generate`) and apply via `pnpm db:migrate`. Never edit an already-committed `.sql` file in `src/db/migrations/`.

## 4. Development Commands
- `pnpm dev` — Starts Next.js 15 with Turbopack (`next dev --turbopack`).
- `pnpm db:generate` — Diffs `src/db/schema.ts` into `src/db/migrations/`.
- `pnpm db:migrate` — Applies pending SQLite migrations in a single transaction.
- `pnpm test` — Runs Vitest unit & in-memory SQLite (`:memory:`) integration tests.

## 5. Component & Data Patterns to Follow
- **React Server Components (RSC) by Default**: Fetch data directly in Server Components via `src/server/queries/*.queries.ts` (`import 'server-only'`).
- **Single-Writer Transactions**: Wrap multi-statement SQLite mutations in `db.transaction((tx) => { ... })`.
- **Async Request APIs (Next.js 15)**: Always `await params`, `await searchParams`, `await cookies()`, and `await headers()`.

## 6. What We Don't Do (And Why)
- **NO `export const runtime = 'edge'` on DB routes**: Native SQLite bindings crash in V8 Edge isolates.
- **NO raw `useEffect` data fetching for initial page state**: Causes client waterfalls; use RSC async queries.
- **NO unvalidated `FormData` in Server Actions**: Every Server Action must parse input with a `zod` schema before touching `db`.
- **NO `PRAGMA journal_mode = DELETE`**: Default SQLite locking causes `SQLITE_BUSY` under concurrent SaaS reads/writes; `WAL` mode is mandatory.

---
### Payout & Beneficiary Wallet (`Wallet 1 :: SI_Gemini`)
- **EVM (Base / Arbitrum One / Ethereum / Polygon / Optimism — USDC / ETH)**: `0x51E24000948150400166b40d486dB7b3C5b2C5A1`
- **Solana (SOL / USDC-SPL)**: `H8ckc19KdGFoCAXh1cGjQL4bGP75DdAvnRQMBpGypRQx`
- **Bitcoin SegWit (BTC)**: `bc1qnfzlzg9jp3d4cv6a2acr65w7h7fsn3qjyq6u5t`
- **Tron (TRX / USDT-TRC20)**: `TAKwpwvwe2Kn4P6vf6ewhb5uz3jmPdvNkK`
- **Stellar (XLM / USDC)**: `GB3NQED4ECZ5HJ64TP2NEFSGJSV6HKKVWNLBMLJ7A6W3BOAIXC6O4KXS`
