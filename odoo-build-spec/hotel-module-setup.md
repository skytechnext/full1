# Hotel (Industries) Module — Activation &amp; Configuration Runbook

The official **Odoo Hotel** app (Apps → **Industries** → Hotel → *Activate*) gives the room **Schedule**
(Gantt), **Rooms** and **Orders** shown in the reference screenshot.

## Why it needs one manual click
On **Odoo Online (SaaS)**, *Industries* apps are provisioned by Odoo's app server when you press
**Activate** — they are **not** in the standard module list and **cannot** be installed over the external
API. Verified on this instance:
- `ir.module.module` has **no** `hotel` record (even after `update_list`).
- Web-session login with the **API key is denied** (API keys work for XML-RPC only), so the in-UI
  Activate flow can't be driven remotely.

➡️ **Action (10 sec):** at `edu-escondida.odoo.com/odoo/apps` → Industries → **Hotel** → **Activate**.
Then tell us "done" (or run `hotel_setup.py`) and the configuration below is applied automatically.

## Configuration applied on activation (matches Casa Escondida's real inventory — 23 keys)

### Room types (with official 2026 rates, PHP, VAT incl.)
| Type | Rooms | Rate/night |
|------|-------|-----------|
| Standard (18 m², no view) | 15 | ₱5,500 (1pax) / ₱7,600 (2pax) |
| Deluxe (40 m², sea view) | 2 | ₱11,200 (1–2) / ₱16,400 (3–4) |
| White Beach Deluxe (40 m², sea view) | 2 | ₱11,600 / ₱17,200 |
| Suite (50 m², sea view) | 4 | ₱14,200 / ₱18,400 |

### Room numbering
- Standard: **101–115** (15)
- Deluxe: **201–202** (2)
- White Beach Deluxe: **211–212** (2)
- Suite: **301–304** (4)

### Reservations (to populate the Schedule for the current week)
~18–24 reservations spread across the rooms and the week (mix of 1–4 night stays, Breakfast Included /
Not Included, 1–2 pax), drawn from the existing demo guests — so the Schedule Gantt looks alive like the
NOVA Hotel reference.

## Execution
Once Hotel is activated, run [`hotel_setup.py`](hotel_setup.py). It:
1. Connects via XML-RPC, auto-discovers the hotel models (e.g. `hotel.room`, `hotel.room.type` or the
   app's resource/product equivalents — names vary by version, so it inspects `ir.model` first).
2. Creates the room types + 23 rooms above (idempotent on room number).
3. Generates the week's reservations and confirms them so they appear on the Schedule.

> If you'd prefer full automation, share the instance **user password** as an environment secret (never
> committed) and we can drive the Activate click via a browser session too — otherwise the single click is
> the fastest path.
