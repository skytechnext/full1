#!/usr/bin/env python3
"""
Replicate the self-contained index.html as the Odoo website HOMEPAGE — verbatim.

Why this approach (and not "paste into the website editor"): index.html is a single ~3.6 MB
self-contained page with its own <head>, inlined Chart.js + Mermaid, and JavaScript full of
`<`, `&&`, `=>` etc. Pasting that into Odoo's QWeb/website editor runs it through the HTML
sanitizer (strips <script>/<head>) and an XML parser (chokes on the JS) — you'd lose the page.
Serving the file RAW as a published attachment reproduces it byte-for-byte, and we point the
website homepage at it. That is the truest "copy & paste as much as possible".

What it does (idempotent):
  1. Reads ../index.html locally and uploads it as a PUBLIC ir.attachment (mimetype text/html).
  2. The attachment is served at /web/content/<id> — opening it renders index.html exactly.
  3. Best-effort sets the website Homepage URL to that path (field name varies by version);
     ALWAYS prints the URL + the one manual step if the API set isn't supported on this instance.

Auth (never commit secrets):
    export ODOO_URL=...  ODOO_DB=...  ODOO_LOGIN=...  ODOO_API_KEY=********
    python3 website_homepage_setup.py            # apply
    python3 website_homepage_setup.py --dry-run   # no connection; explain the plan
"""
import os, sys, base64, xmlrpc.client

DRY = "--dry-run" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.normpath(os.path.join(HERE, "..", "index.html"))
ATT_NAME = "casa-escondida-report.html"

if DRY:
    sz = os.path.getsize(INDEX) if os.path.exists(INDEX) else 0
    print("\n=== REPLICATE index.html → Odoo homepage (DRY RUN) ===\n")
    print(f"Source        : {INDEX} ({sz/1_048_576:.2f} MB)")
    print(f"Upload as     : public ir.attachment '{ATT_NAME}' (mimetype text/html)")
    print( "Served at     : /web/content/<id>  (renders index.html verbatim)")
    print( "Homepage      : set website Homepage URL to that path (best-effort; manual fallback printed)")
    print( "Idempotent    : re-running refreshes the attachment content in place")
    print("\nRun without --dry-run (with ODOO_* env set) to apply.\n")
    sys.exit(0)

if not os.path.exists(INDEX):
    sys.exit(f"index.html not found at {INDEX}")
KEY = os.environ.get("ODOO_API_KEY")
if not KEY:
    sys.exit("Set ODOO_API_KEY in the environment first (or use --dry-run). Never commit it.")
URL = os.environ.get("ODOO_URL", "https://edu-escondida.odoo.com")
DB = os.environ.get("ODOO_DB", "edu-escondida")
LOGIN = os.environ.get("ODOO_LOGIN", "sky@technext.asia")

common = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/common", allow_none=True)
UID = common.authenticate(DB, LOGIN, KEY, {})
if not UID:
    sys.exit("Authentication failed — check ODOO_DB / ODOO_LOGIN / ODOO_API_KEY.")
M = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/object", allow_none=True, use_datetime=True)
def x(model, method, args=None, kw=None):
    return M.execute_kw(DB, UID, KEY, model, method, args or [], kw or {})
def has_field(model, field):
    try: return field in x(model, "fields_get", [[field], ["type"]])
    except Exception: return False

print(f"Connected uid={UID} @ {URL} ({DB})")
data = base64.b64encode(open(INDEX, "rb").read()).decode()
print(f"Read index.html ({len(data)*3//4/1_048_576:.2f} MB) — uploading…")

# 1) idempotent public attachment (public-flag field name varies: 'public' vs 'is_public')
pub_field = "public" if has_field("ir.attachment", "public") else ("is_public" if has_field("ir.attachment", "is_public") else None)
base = {"name": ATT_NAME, "datas": data, "mimetype": "text/html", "type": "binary"}
if pub_field: base[pub_field] = True
found = x("ir.attachment", "search", [[["name", "=", ATT_NAME]]], {"limit": 1})
if found:
    att_id = found[0]
    wr = {"datas": data, "mimetype": "text/html"}
    if pub_field: wr[pub_field] = True
    x("ir.attachment", "write", [found, wr]); print(f"attachment refreshed (id={att_id})")
else:
    att_id = x("ir.attachment", "create", [base]); print(f"attachment created (id={att_id})")

served = f"/web/content/{att_id}"
public_url = URL.rstrip("/") + served

# 2) best-effort: point the website homepage at it (field/behaviour varies by version)
set_ok = False
try:
    sites = x("website", "search", [[]], {"limit": 1})
    if sites:
        for field in ("homepage_url", "homepage"):   # 16+/older variants
            if has_field("website", field):
                try:
                    x("website", "write", [sites, {field: served}]); set_ok = True
                    print(f"website.{field} set → {served}"); break
                except Exception as e:
                    print(f"note: could not set website.{field}: {str(e)[:90]}")
except Exception as e:
    print(f"note: website homepage set skipped: {str(e)[:90]}")

print("\n=== DONE ===")
print(f"index.html is now served verbatim at:\n  {public_url}")
if set_ok:
    print("It is set as the website homepage — visit the site root to confirm.")
else:
    print("Could not set the homepage automatically on this instance. One manual step:")
    print("  Odoo → Website → Settings → 'Homepage URL' = " + served)
    print("  (or add a top-menu item linking to it).")
print("\nRe-run anytime to push an updated index.html (idempotent).")
