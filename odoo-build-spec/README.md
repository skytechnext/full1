# Casa Escondida Anilao — Odoo 19 Build Spec (MCP-ready)

This folder is a **machine-readable, executable specification** for building the Casa Escondida
Anilao Resort & Dive Center ERP on **Odoo 19**, pre-loaded with extensive demo data. It is designed
so that an AI agent connected to an **Odoo MCP server** can execute it end-to-end with minimal
human input.

> **Status:** No Odoo MCP server is connected in the session that produced this spec. This is the
> "next step" deliverable — connect an Odoo 19 instance via MCP, then run the agent loop in
> [`../agents/orchestration.md`](../agents/orchestration.md) against this spec.

## Files

| File | Purpose |
|------|---------|
| `modules.json` | The 8–12 modules + install order, rationale, gaps, recommended add-ons. |
| `data-model.json` | Per-module models, fields, Studio (`x_`) fields, naming. |
| `demo-data.json` | Master + transactional demo data with record counts & realism rules. |
| `automations.json` | Native Odoo automations + external AI-agent automations. |
| `mcp-runbook.md` | The exact ordered MCP call sequence (9 stages) + idempotency rules. |

## How an AI agent should use this

1. **Connect** to the Odoo 19 instance via the Odoo MCP server (verify with a `res.company` read).
2. **Read** `modules.json` → install modules in `install_order`.
3. **Follow** `mcp-runbook.md` stage by stage. Each stage has a verification query; do not advance
   until it passes (this is the loop — see `agents/orchestration.md`).
4. **Apply idempotency rules** (below) on every create.
5. **Load** demo data from `demo-data.json` (generate realistic values within the rules).
6. **Configure** automations from `automations.json` (native first; AI hooks are external).

## Idempotency rules (critical — re-runs must not duplicate)

- **Search before create.** Look up by a natural key first; update or skip if found:
  - products → `default_code`
  - rooms → `stock.lot.name` (e.g. `STD-01`)
  - partners → `email` (fallback `name` + `phone`)
  - sale orders → `client_order_ref` (`CE-<channel>-<seq>`)
- Use the `default_code` / lot-name **prefixes** in the spec so identity is stable across runs.
- **Strict ordering:** chart of accounts + taxes → currencies → pricelists → partners → products →
  resources → orders → confirm → invoice → register payment. Never invoice before the CoA/taxes exist.
- **Two-pass confirm/post:** create all drafts first, then confirm/post in a separate pass so a failed
  batch can resume without re-creating drafts.
- **Cache lookups** (tax ids, account ids, pricelist ids, partner ids) before referencing them.

## Out of scope / flagged gaps

- **PMS depth** (room-status board, night audit): Rental-core covers availability; OCA `hotel` or a
  custom `room.reservation` Gantt is the upgrade path.
- **OTA channel-sync**: needs a third-party channel manager or custom integration; demo simulates it
  with the `x_channel` field + overbooking-guard scheduled action.
