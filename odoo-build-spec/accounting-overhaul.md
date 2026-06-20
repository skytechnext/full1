# Accounting Overhaul — Odoo 19 build spec

Operationalises the automation-first finance plan (the web page `../accounting-revamp.html`) into
concrete Odoo configuration. The achievable-over-API pieces are applied by **`accounting_setup.py`**
(idempotent, env-driven, `--dry-run` to preview). The rest are flagged as manual (browser/accountant).

> Connect per `connection.md` (Tier 2 API is enough for everything here). Secrets via env, never committed.

## What `accounting_setup.py` configures
| Area | Odoo model(s) | What it does | Idempotent key |
|---|---|---|---|
| Profit-centre analytics | `account.analytic.plan`, `account.analytic.account` | Plan "Profit centre" + accounts Rooms/Dive/Restaurant/Retail/Courses → live per-department P&L | name |
| VAT | `account.tax` | **Verifies** the 12% Sales/Purchase VAT already in use (does not duplicate) | amount=12 |
| Journals | `account.journal` | BPI/BDO/GCash (bank), Cash, Petty Cash | code |
| Deferred & statutory liabilities | `account.account` | Customer Deposits (deferred revenue), Gift Cards/Vouchers, Withholding Tax Payable | code |
| Bank automation | `account.reconcile.model` | Scaffolds for bank charges / GCash fees (set match rules in-app) | name |
| Withholding | `account.fiscal.position` | EWT scaffold (full EWT needs `l10n_ph_withholding` + accountant) | name |
| POS room-charge | `pos.payment.method` | "Room Charge" so F&B/dive push to the guest folio | name |

Run order: it is order-independent and safe to re-run; field/model names are **discovered** at runtime
(`fields_get`) so it adapts across Odoo versions, and every create is guarded + searched-first.

## Maps to the workflows (see `../accounting-revamp.html`)
- **Order-to-Cash** — folio→invoice + POS session→journal are native once apps post to the ledger;
  this spec adds the **Room Charge** POS method + profit-centre tagging + deferred-revenue liability.
- **Procure-to-Pay** — AI bill capture/3-way match are native Purchase+Accounting; this spec adds the
  **EWT fiscal-position** scaffold and **Withholding Tax Payable** account.
- **Bank & cash** — this spec adds the bank/GCash/cash **journals** + **reconciliation-model** scaffolds.
- **Department P&L** — the **analytic plan** is the engine; tag products/departments so postings inherit it.
- **Revenue recognition** — **Customer Deposits** + **Gift Cards/Vouchers** liability accounts; set
  deferred-revenue on the relevant products/journals in-app.

## Manual — cannot be done over the API
1. **BIR accreditation** of the Odoo CAS and POS machines; approved sequential invoice series. The old POS
   accreditation has lapsed — this gates go-live selling. (browser + BIR RDO)
2. **Chart-of-accounts swap to `l10n_ph`** — blocked while posted entries exist; needs an **empty-books
   cutover** (fresh fiscal period or fresh DB seeded with opening balances). See the cutover plan on the
   web page §15.
3. **Expanded withholding tax (proper)** — install `l10n_ph_withholding` (or equivalent) and configure tax
   mappings + Form 2307 with your accountant.
4. **EIS e-invoicing** enrolment if/when the business is mandated.

## Runbook integration
This extends `mcp-runbook.md` **Stage 2 (company/tax/finance)** and **Stage 8 (automations)**:
- Stage 2: after taxes/journals, run `accounting_setup.py` to add analytics, liability accounts, and the
  reconciliation/EWT/POS scaffolds.
- Stage 8: dynamic-pricing / review / guard automations already covered there; the finance reconciliation
  models and recurring entries (depreciation, deferred revenue) are configured here + in-app.

## Verify
- `python3 accounting_setup.py --dry-run` prints the plan and exits 0 with no connection (CI-safe).
- Against an instance: re-running reports `skipped(idempotent)` for everything already present (no dupes).
- Check Accounting → Configuration: analytic plan "Profit centre" (5 accounts), the 5 journals, the 3
  liability accounts, the reconciliation models, the EWT fiscal position; POS shows "Room Charge".
