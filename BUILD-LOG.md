# Live Odoo Build Log — edu-escondida.odoo.com

Built directly over the Odoo external API (XML-RPC) on **Odoo 19 Enterprise**.
DB `edu-escondida`, user `sky@technext.asia`. The API token was used only at runtime and **never committed**
(it was deleted locally after the build — **rotate it**).

## Apps installed (17)
account, l10n_ph, point_of_sale, pos_restaurant, stock, stock_barcode, sale_management, crm, hr, hr_skills,
maintenance, project, calendar, contacts, **website, website_sale**, mail.

## Configuration
- Company renamed **Casa Escondida Anilao Resort & Dive Center**; currency **PHP**; country **Philippines**; logo set.
- **VAT 12%** + **Input VAT 12%** taxes created and applied to products & invoices.
- `l10n_ph` installed (PH localization data available). NOTE: the active chart of accounts could **not** be
  swapped to the PH template because posted journal entries already exist — that requires an empty-books window;
  12% VAT is in use in the meantime.
- POS config "Casa Escondida — Restaurant & Dive Shop" with Cash / Card / Customer Account payment methods.
- Website published; PWA is native to the Odoo 19 website frontend.

## Demo data generated (with images / text / entries)
| Object | Count |
|---|---|
| Products (CE-, all with generated images) | 42 |
| Products published to eCommerce `/shop` | 42 |
| Website pages (Book, Dive Center, Restaurant, Events + shop) | 9 |
| Customers (persona-tagged, multi-country) | 40 |
| Vendors | 10 |
| Employees / Departments | 37 / 9 |
| Sale orders (28 confirmed, ~₱1.76M) | 45 |
| CRM opportunities | 30 |
| Customer invoices posted | 18 |
| Vendor bills posted | 10 |
| POS orders (paid) | 36 (~₱176k) |
| Maintenance equipment / requests | 14 / 5 |
| Course projects / tasks | 4 / 17 |
| Pricelists | 2 |

## Public URLs (live)
- Shop / online booking: https://edu-escondida.odoo.com/shop
- https://edu-escondida.odoo.com/book · /dive-center · /restaurant · /events
- Backend: https://edu-escondida.odoo.com/odoo

## Not done via API (require manual app install / subscription)
- **Webkul Hotel/PMS** (paid) and **QloApps Channel Manager** — must be purchased/uploaded to the instance and
  a QloApps subscription activated; cannot be installed over the API. Rooms are currently modelled as priced,
  bookable eCommerce products. Spec in `odoo-build-spec/`.
- **Chart-of-accounts swap to l10n_ph** — needs an empty-books window (see above).

## Update — 14 Jun 2026 (round 2)
- **Currency**: switched everything SGD→**PHP** (company, both pricelists incl. Default); **SGD deactivated**.
- **Apps removed**: **To-do** (project_todo) uninstalled. **Discuss** menu hidden (the `mail` module is a core
  framework dependency of CRM/Sales/HR/Website, so it cannot be uninstalled without removing them — its app
  menu is deactivated instead).
- **POS upgraded**: two configs — *Restaurant & Room Service* and *Dive Shop & Retail*. Restaurant has a
  **floor plan**: 4 floors (Open-Air Dining, Beachfront Deck, Bar Lounge, Pool Deck) with **23 laid-out tables**.
- **Inventory tracking**: F&B/bar/retail/Nitrox set **storable** (17 products) with initial on-hand stock; POS sales decrement stock.
- **Automations**: **7 scheduled actions** (dynamic pricing, dive daily briefing, overbooking guard, post-stay
  review, low-stock reorder, cert renewals, win-back) + **1 automated rule** (welcome message on booking confirmation).
- **Branding/media**: real **room photos** from the website set on room products; **company logo** set (logo-color).
- Restaurant, hotel (rooms) and dive center are all represented with products, images, stock, POS and pages.

## Report site (GitHub Pages) — round 2
- Header controls (search/theme/install) moved into the **toggleable hamburger sidebar**; top bar shows the
  **Casa Escondida white logo**. Mobile sidebar slides in as an overlay. PDF button removed (earlier). 
- Diagrams made responsive (Daily automation flow scrolls/scales on mobile). Full **PWA** (installable, offline).
