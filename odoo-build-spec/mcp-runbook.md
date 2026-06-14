# MCP Runbook — Odoo 19 Build Execution Sequence

The exact, ordered sequence an AI agent executes against an **Odoo MCP server** to build the Casa
Escondida ERP and load demo data. Nine stages. Each stage lists its actions and a **verification
query** that must pass before advancing. Honour the idempotency rules in `README.md` throughout.

Typical Odoo MCP primitives assumed: `search_read(model, domain, fields)`,
`create(model, values)`, `write(model, ids, values)`, `call_method(model, method, args)`,
`install_modules(names)`. Adapt names to the connected server.

---

## Stage 0 — Connect & preflight
- Read `res.company` to confirm connectivity and DB identity.
- Detect Odoo version (expect 19) and already-installed modules.
- **Verify:** `res.company` returns ≥1 record.

## Stage 1 — Install modules
- Install `modules.json:install_order` in sequence (dependencies resolve automatically).
- Install `recommended_addons` (sign, documents, knowledge, marketing_automation, mass_mailing).
- **Verify:** every `tech_name` appears in installed modules.

## Stage 2 — Company, currency, tax, finance
- Set company name/address/timezone (`Asia/Manila`); base currency `PHP`; activate `USD`, `EUR`.
- Install `l10n_ph` chart of accounts; create the 4 taxes (`TAX-S12`, `TAX-P12`, `TAX-EX`).
- Create journals (sales, purchase, bank, cash, misc, POS) and fiscal year/sequences.
- Create pricelists `PL-PEAK`, `PL-OFF`.
- **Verify:** sales VAT 12% tax exists; `account.account` count > 50; both pricelists exist.

## Stage 3 — Master data (partners & people)
- Create `res.partner.category` persona tags; create ~150 customers, 3 OTA partners, 5 agencies, 20 vendors.
- Create `hr.department` (8) and ~30 `hr.employee`; attach PADI/EFR skills + renewal dates.
- Create dive-site taxonomy (~35) and `calendar.resource` (boats, instructor/DM pools).
- **Verify:** customers ≥ 150; employees ≥ 30; departments = 8.

## Stage 4 — Products & rooms
- Create room-type templates (3) with `rent_ok=true`, `tracking=serial`; generate 31 `stock.lot` serials (`STD/DLX/SVS`).
- Create the Studio `x_` fields on `sale.order` (channel, adults, children, meal_plan, season) **before** any order.
- Create dive-trip products (6), course products (7), gear rental products (12) + ~100 serial units, consumables (8), F&B menu (60), retail (40).
- Link gear serials to `maintenance.equipment`; set preventive plans.
- **Verify:** room serials = 31; products with required `default_code` prefixes exist; `x_channel` field present on `sale.order`.

## Stage 5 — POS & booking setup
- Create POS configs: `Restaurant` (with `pos_restaurant`, 3 floors, 20 tables) and `Dive Shop Retail`.
- Create payment methods incl. **Room Charge**.
- Create `appointment.type` for dive trips with resource capacity.
- **Verify:** 2 POS configs; Room Charge method exists; ≥4 appointment types.

## Stage 6 — Transactions (draft pass)
- Generate within 2025-12-01 → 2026-05-31, honouring seasonality & persona mix:
  - ~200 room reservations (Rental orders) across channels/room types/pricelists.
  - ~300 dive bookings (calendar events + sale order lines).
  - ~40 course cohorts (events/projects) with Sign waivers.
  - ~150 gear rentals; ~2000 POS orders (restaurant + retail).
  - ~80 CRM leads / ~50 opportunities with stages & sources.
- **Verify:** sale.order count ≥ 600; pos.order count ≥ 1500; crm.lead ≥ 80.

## Stage 7 — Transactions (confirm/invoice/pay pass)
- Confirm sale orders; generate ~400 customer invoices (VAT 12%); ~120 vendor bills.
- Register payments for ~80% (leave ~20% open for realistic AR/AP aging).
- Close sample POS sessions so they post to accounting.
- Issue ~35 certifications (Documents); create ~40 maintenance requests (mix preventive/corrective).
- **Verify:** posted invoices ≥ 350; payments registered; VAT report non-empty.

## Stage 8 — Automations & dashboards
- Configure native automations from `automations.json:native_automations` (Studio/scheduled/server actions).
- Register external AI hooks (`ai_agent_automations`) as documented endpoints (no live external calls in demo).
- Configure dashboards listed in `demo-data.json:dashboards_to_configure`.
- **Verify:** scheduled actions exist for pricing, overbooking guard, review request; dashboards render.

## Stage 9 — Final QA
- Run cross-module spot-checks: a booking with room + dive + F&B room-charge → single invoice; a gear
  serial in maintenance is unavailable in Rental; a course cohort has a completed waiver + cert.
- Produce a build report: record counts vs. `demo-data.json` targets, and any deviations.
- **Verify:** all stage verifications green; counts within ±10% of targets.

---

### Resume / failure handling
- On any failure, re-run the current stage — idempotency rules make creates safe to repeat.
- Keep a run-log of created external IDs so partial progress is detectable.
- The orchestration loop (`agents/orchestration.md`) wraps these stages and only advances on green verification.
