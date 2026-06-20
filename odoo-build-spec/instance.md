# Live Build Instance — edu-escondida.odoo.com

The Odoo 19 build target for Casa Escondida.

## Connection

**Full strategy + fallback logic is in [`connection.md`](connection.md). Summary:**

| Tier | Path | Works on | Use for |
|---|---|---|---|
| 1 (preferred) | **Odoo.sh SSH** → `odoo shell` (`env`), git deploy | Odoo.sh only | bulk server-side build, custom modules, logs |
| 2 (fallback) | **Credentials / API** (XML-RPC/JSON-RPC, via MCP) | any instance | most record CRUD, standard installs |
| 3 (last resort) | **Browser** (Playwright) | any instance | SaaS *Activate*/Industry install, some Studio |

- **Current demo URL:** https://edu-escondida.odoo.com/odoo — an Odoo **Online / SaaS** education
  instance, so **no SSH**; it was built via Tier 2 (API) + Tier 3 (browser, for the Hotel-industry
  install). For the real build, an **Odoo.sh** project unlocks Tier 1 (the most capable path).
- **Secrets** (API key, SSH key, login) are supplied **out-of-band** and stored as env / MCP config —
  🔒 **never commit them.** Env the helpers read: `ODOO_URL`, `ODOO_DB`, `ODOO_LOGIN`, `ODOO_API_KEY`
  (Tier 2) and `ODOO_SH_HOST` (Tier 1). If any was shared in plaintext, **rotate it.**
- **Pick the tier automatically:** `python connect/probe.py`.

## Build sequence (summary — full detail in `mcp-runbook.md`)

1. **Stage 0 — Reset:** delete all old/demo items first (client instruction). Prefer marker-based
   deletion so real data is safe; on a fresh education DB a neutralize+empty reload is cleanest
   (confirm before destructive deletes).
2. **Install** modules per `modules.json` (Phase 1 = POS + Inventory + Accounting first), incl. the
   **Webkul Hotel/PMS** and **`hotel_qloapps_channel_manager`** apps.
3. **Configure** company/PHP/12% VAT/BIR receipts; `PL-BASE` flat rates (+ optional `PL-VARIABLE`).
4. **Generate demo data** per `demo-data.json` — **pictures, items, text and entries** — across 23 rooms,
   dive/courses/F&B/retail, ~36 staff, ~150 guests, and ~Dec 2025–May 2026 transactions.
5. **Automations & dashboards** per `automations.json`.
6. **QA** per `mcp-runbook.md` Stage 9; emit a build report (counts vs targets).

## Demo media (pictures)

Generate/assign images so the system looks alive:
- Room-type photos (Standard/Deluxe/White Beach Deluxe/Suite), restaurant, pool, jetty, dive boats, gear.
- Product images for F&B menu and retail.
- Employee avatars; company logo (Casa Escondida).
- Source from the client's website/gallery where licensed, or use neutral placeholders tagged
  `x_demo_media=true` so they're easy to swap for real assets later.

## Safety checklist before running on the live instance

- [ ] Confirm `edu-escondida.odoo.com` is the intended education/sandbox DB (not production).
- [ ] Backup / snapshot the DB before Stage 0 deletes.
- [ ] Token stored as a secret, not in git.
- [ ] Destructive reset confirmed with Andrew/Dong.
- [ ] BIR-accreditation path for POS confirmed before any real selling.
