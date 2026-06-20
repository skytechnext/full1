#!/usr/bin/env python3
"""
Configure the ACCOUNTING OVERHAUL for Casa Escondida on Odoo 19.

Implements the automation-first finance plan (see ../accounting-revamp.html and
accounting-overhaul.md) — the pieces that are achievable over the external API:
analytic "Profit centre" plan + accounts, bank/GCash/cash journals, deferred-revenue
and statutory liability accounts, reconciliation-model scaffolds, an EWT fiscal-position
scaffold, and the POS "Room Charge" payment method. It VERIFIES (not duplicates) the
12% VAT that is already in use.

It is DEFENSIVE and IDEMPOTENT: it discovers model/field names first (they differ across
Odoo versions), searches before it creates, and prints exactly what it did or skipped.

Browser-only / accountant steps it CANNOT do over the API (it reminds you):
  * BIR accreditation of the Odoo CAS and POS machines + approved invoice series
  * Swapping the active chart of accounts to the l10n_ph template (needs empty books)
  * Proper expanded-withholding tax (install l10n_ph_withholding / configure with your accountant)
  * EIS e-invoicing enrolment

Auth (never hard-code / commit secrets):
    export ODOO_URL=...  ODOO_DB=...  ODOO_LOGIN=...  ODOO_API_KEY=********
    python3 accounting_setup.py            # apply against the instance
    python3 accounting_setup.py --dry-run  # print the plan only; no connection, no key needed
"""
import os, sys, xmlrpc.client

DRY = "--dry-run" in sys.argv

URL = os.environ.get("ODOO_URL", "https://edu-escondida.odoo.com")
DB = os.environ.get("ODOO_DB", "edu-escondida")
LOGIN = os.environ.get("ODOO_LOGIN", "sky@technext.asia")
KEY = os.environ.get("ODOO_API_KEY")

# ---- planned configuration (also printed by --dry-run) ----
PROFIT_CENTRES = ["Rooms", "Dive", "Restaurant", "Retail", "Courses"]
JOURNALS = [  # (name, code, type)
    ("BPI Bank", "BPI", "bank"),
    ("BDO Bank", "BDO", "bank"),
    ("GCash", "GCASH", "bank"),
    ("Cash", "CSH", "cash"),
    ("Petty Cash", "PETTY", "cash"),
]
LIABILITY_ACCOUNTS = [  # (name, code, account_type)
    ("Customer Deposits (deferred)", "215000", "liability_current"),
    ("Gift Cards / Vouchers", "216000", "liability_current"),
    ("Withholding Tax Payable", "217000", "liability_current"),
]
RECON_MODELS = ["Bank charges", "GCash fees"]   # write-off suggestion scaffolds
EWT_FISCAL_POSITION = "EWT — Suppliers (PH withholding)"
POS_PAYMENT = "Room Charge"

SUMMARY = []
def note(action, detail=""):
    SUMMARY.append((action, detail))
    print(f"  {action:<10} {detail}")

if DRY:
    print("\n=== ACCOUNTING OVERHAUL — DRY RUN (no connection) ===\n")
    print("Profit-centre analytic accounts:", ", ".join(PROFIT_CENTRES))
    print("Journals:", ", ".join(f"{n} [{c}/{t}]" for n, c, t in JOURNALS))
    print("Liability accounts:", ", ".join(f"{n} ({c})" for n, c, _ in LIABILITY_ACCOUNTS))
    print("Reconciliation-model scaffolds:", ", ".join(RECON_MODELS))
    print("EWT fiscal position:", EWT_FISCAL_POSITION)
    print("POS payment method:", POS_PAYMENT)
    print("\nVerify-only: 12% Sales/Purchase VAT (already in use).")
    print("\nManual (browser/accountant): BIR CAS+POS accreditation; l10n_ph CoA swap (empty books);")
    print("expanded-withholding via l10n_ph_withholding; EIS e-invoicing enrolment.")
    print("\nRun without --dry-run (with ODOO_* env set) to apply, idempotently.\n")
    sys.exit(0)

if not KEY:
    sys.exit("Set ODOO_API_KEY in the environment first (or use --dry-run). Never commit it.")

common = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/common", allow_none=True)
UID = common.authenticate(DB, LOGIN, KEY, {})
if not UID:
    sys.exit("Authentication failed — check ODOO_DB / ODOO_LOGIN / ODOO_API_KEY.")
M = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/object", allow_none=True, use_datetime=True)
def x(model, method, args=None, kw=None):
    return M.execute_kw(DB, UID, KEY, model, method, args or [], kw or {})
def has_model(model):
    return bool(x("ir.model", "search_count", [[["model", "=", model]]]))
def fields_of(model):
    try: return x(model, "fields_get", [[], ["type", "string", "selection"]])
    except Exception: return {}
def ensure(model, domain, vals, label):
    """Idempotent: skip if a record matching `domain` exists, else create."""
    try:
        found = x(model, "search", [domain], {"limit": 1})
        if found:
            note("skip", f"{label} (exists)"); return found[0]
        rid = x(model, "create", [vals])
        note("create", label); return rid
    except Exception as e:
        note("note", f"{label}: {str(e)[:130]}"); return None

print(f"Connected uid={UID} @ {URL} ({DB})\n")

# ---- 1. Analytic 'Profit centre' plan + accounts ----
print("1) Profit-centre analytic accounts")
plan_id = None
if has_model("account.analytic.plan"):
    plan_id = ensure("account.analytic.plan", [["name", "=", "Profit centre"]],
                     {"name": "Profit centre"}, "plan: Profit centre")
aaf = fields_of("account.analytic.account")
for pc in PROFIT_CENTRES:
    vals = {"name": pc}
    if plan_id and "plan_id" in aaf: vals["plan_id"] = plan_id
    ensure("account.analytic.account", [["name", "=", pc]], vals, f"analytic: {pc}")

# ---- 2. Verify 12% VAT (do not duplicate) ----
print("2) VAT verification")
try:
    vat = x("account.tax", "search_read", [[["amount", "=", 12.0]]], {"fields": ["name", "type_tax_use"], "limit": 5})
    note("verify", f"{len(vat)} x 12% taxes present: " + ", ".join(t["name"] for t in vat) if vat else "no 12% tax found — configure VAT")
except Exception as e:
    note("note", f"tax check: {str(e)[:120]}")

# ---- 3. Bank / GCash / cash journals ----
print("3) Journals")
for name, code, jtype in JOURNALS:
    ensure("account.journal", [["code", "=", code]],
           {"name": name, "code": code, "type": jtype}, f"journal: {name} [{code}]")

# ---- 4. Deferred-revenue & statutory liability accounts ----
print("4) Liability accounts")
acf = fields_of("account.account")
type_field = "account_type" if "account_type" in acf else ("user_type_id" if "user_type_id" in acf else None)
for name, code, atype in LIABILITY_ACCOUNTS:
    vals = {"name": name, "code": code}
    if type_field == "account_type":
        vals["account_type"] = atype
    ensure("account.account", [["code", "=", code]], vals,
           f"account: {name} ({code})" + ("" if type_field == "account_type" else " [set type manually]"))

# ---- 5. Reconciliation-model scaffolds ----
print("5) Reconciliation models")
if has_model("account.reconcile.model"):
    rmf = fields_of("account.reconcile.model")
    for nm in RECON_MODELS:
        vals = {"name": nm}
        # rule_type varies by version; 'writeoff_suggestion' is the common auto-suggest type
        if "rule_type" in rmf: vals["rule_type"] = "writeoff_suggestion"
        ensure("account.reconcile.model", [["name", "=", nm]], vals, f"recon model: {nm}")
    note("note", "Open Accounting → Configuration → Reconciliation Models to set match rules + counterpart accounts.")
else:
    note("note", "account.reconcile.model not available on this instance")

# ---- 6. EWT fiscal-position scaffold ----
print("6) Withholding (EWT) scaffold")
ensure("account.fiscal.position", [["name", "=", EWT_FISCAL_POSITION]],
       {"name": EWT_FISCAL_POSITION}, f"fiscal position: {EWT_FISCAL_POSITION}")
note("note", "Proper EWT needs l10n_ph_withholding (or accountant config) + tax mappings + Form 2307.")

# ---- 7. POS 'Room Charge' payment method ----
print("7) POS payment method")
if has_model("pos.payment.method"):
    ensure("pos.payment.method", [["name", "=", POS_PAYMENT]],
           {"name": POS_PAYMENT}, f"pos payment: {POS_PAYMENT}")
else:
    note("note", "pos.payment.method not available (install Point of Sale)")

# ---- summary ----
print("\n=== SUMMARY ===")
created = sum(1 for a, _ in SUMMARY if a == "create")
skipped = sum(1 for a, _ in SUMMARY if a == "skip")
print(f"created={created}  skipped(idempotent)={skipped}  notes={sum(1 for a,_ in SUMMARY if a=='note')}")
print("\nStill MANUAL (browser/accountant, cannot be done over the API):")
print("  • BIR accreditation of the Odoo CAS + POS machines; approved invoice series (old accreditation lapsed)")
print("  • Swap active chart of accounts to l10n_ph (needs an EMPTY-BOOKS window — pick a fiscal-period cutover)")
print("  • Expanded withholding tax proper: install l10n_ph_withholding / configure with your accountant")
print("  • EIS e-invoicing enrolment if/when the business is mandated")
print("\nNext: tag products with their profit centre + set deferred-revenue on guest-deposit products,")
print("then add bank-statement imports and reconciliation rules. See accounting-overhaul.md.")
