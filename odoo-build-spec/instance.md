# Live Build Instance — edu-escondida.odoo.com

The Odoo 19 build target for Casa Escondida.

## Connection

- **URL:** https://edu-escondida.odoo.com/odoo
- **Access credential:** supplied by the client **out-of-band** (a token/hash was provided in chat).
  - 🔒 **Do NOT commit the token to this repository or any file.** Store it as an environment secret
    (e.g. `ODOO_MCP_TOKEN`) or in the Odoo MCP server's config only.
  - If it was ever shared in plaintext, treat it as exposed and **rotate it** after the build.
- The executing agent connects through an **Odoo MCP server** pointed at this URL with that secret.
  No Odoo MCP server is attached to the planning session that produced this spec — attach one to run.

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
