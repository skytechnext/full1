# Replicate index.html as the Odoo website homepage

Goal: make the resort's Odoo website serve the self-contained `index.html` (the full strategy report)
**verbatim** as its main page — a true copy, not a re-typed approximation.

## Why "serve raw", not "paste into the editor"
`index.html` is one ~3.6 MB self-contained file: its own `<head>`, inlined Chart.js + Mermaid, and a
lot of JavaScript (`<`, `&&`, `=>`, template literals). Odoo's website/QWeb editor runs pasted markup
through (a) an HTML **sanitizer** that strips `<head>`/`<script>` and (b) an **XML parser** that rejects
the JS. Pasting would destroy the page. Serving the file as a published attachment reproduces it exactly.

## Apply
`odoo-build-spec/website_homepage_setup.py` (idempotent, env-driven, `--dry-run`):
1. Reads `../index.html` and uploads it as a **public** `ir.attachment` (mimetype `text/html`).
2. The attachment renders verbatim at `/web/content/<id>`.
3. Best-effort sets the website **Homepage URL** to that path (field name varies by Odoo version) and
   always prints the URL + the one manual step if the API set isn't supported.

```bash
export ODOO_URL=https://edu-escondida.odoo.com ODOO_DB=edu-escondida \
       ODOO_LOGIN=<login> ODOO_API_KEY=<key>          # rotate the key after
python3 odoo-build-spec/website_homepage_setup.py
```

Re-running pushes an updated `index.html` in place (idempotent — matches the attachment by name).

## Manual fallback (if the homepage field isn't settable via API on this instance)
Odoo → **Website → Settings → Homepage URL** = `/web/content/<id>` (printed by the script), or add a
top-menu link to it.

## Notes
- The companion pages (requirements, quotation, accounting-overhaul, etc.) are linked from inside
  `index.html`; to serve those under Odoo too, upload each the same way (extend the script's list) or
  keep them on GitHub Pages and link out.
- Source of truth for the HTML is this repo's `index.html`; GitHub Pages already publishes the same file.
