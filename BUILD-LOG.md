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
