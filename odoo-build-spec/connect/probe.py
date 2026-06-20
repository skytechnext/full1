#!/usr/bin/env python3
"""Connection health-check / probe — decides which tier the build agent should use.

Tries, in order of capability:
  1. Odoo.sh SSH      (if ODOO_SH_HOST is set and `ssh ... odoo shell` is reachable)
  2. Credentials/API  (if ODOO_URL/ODOO_DB/ODOO_LOGIN/ODOO_API_KEY authenticate)
  3. Browser          (assumed reachable if ODOO_URL is set)

Prints a capability report and the recommended tier. No secrets are printed or stored.
Run:  python connect/probe.py
"""

import os
import shutil
import subprocess
import sys

GREEN, RED, AMBER, DIM, END = "\033[92m", "\033[91m", "\033[93m", "\033[2m", "\033[0m"


def line(ok, label, detail=""):
    mark = f"{GREEN}OK {END}" if ok else f"{RED}-- {END}"
    print(f"  {mark} {label}{('  ' + DIM + detail + END) if detail else ''}")


def probe_ssh():
    host = os.environ.get("ODOO_SH_HOST")  # e.g. mybranch@myproject.dev.odoo.com
    if not host:
        line(False, "Tier 1 · Odoo.sh SSH", "ODOO_SH_HOST not set (skip — SaaS has no SSH)")
        return False
    if not shutil.which("ssh"):
        line(False, "Tier 1 · Odoo.sh SSH", "ssh client not found")
        return False
    try:
        r = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", host, "echo ok"],
            capture_output=True, text=True, timeout=20,
        )
        ok = r.returncode == 0 and "ok" in r.stdout
        line(ok, "Tier 1 · Odoo.sh SSH", host if ok else (r.stderr.strip()[:80] or "unreachable"))
        return ok
    except Exception as e:  # noqa: BLE001
        line(False, "Tier 1 · Odoo.sh SSH", str(e)[:80])
        return False


def probe_api():
    needed = ["ODOO_URL", "ODOO_DB", "ODOO_LOGIN", "ODOO_API_KEY"]
    missing = [k for k in needed if not os.environ.get(k)]
    if missing:
        line(False, "Tier 2 · Credentials / API", "missing env: " + ", ".join(missing))
        return False
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from xmlrpc_client import Odoo  # local import
        o = Odoo.from_env()
        o.authenticate()
        ver = o.version().get("server_version", "?")
        mods = o.count("ir.module.module", [["state", "=", "installed"]])
        line(True, "Tier 2 · Credentials / API", f"uid={o.uid} · Odoo {ver} · {mods} modules installed")
        return True
    except Exception as e:  # noqa: BLE001
        line(False, "Tier 2 · Credentials / API", str(e)[:90])
        return False


def probe_browser():
    url = os.environ.get("ODOO_URL")
    has_pw = bool(shutil.which("node")) or os.path.isdir("/opt/node22/lib/node_modules/playwright")
    ok = bool(url)
    line(ok, "Tier 3 · Browser (Playwright)",
         (f"{url} · playwright={'yes' if has_pw else 'install needed'} · needs login creds") if ok
         else "ODOO_URL not set")
    return ok


def main():
    print(f"\n{AMBER}Odoo connection probe{END} — picking the highest available tier\n")
    ssh_ok = probe_ssh()
    api_ok = probe_api()
    br_ok = probe_browser()

    if ssh_ok:
        tier, why = "ssh", "full server-side ORM/Python, git deploy, no RPC limits"
    elif api_ok:
        tier, why = "api", "XML-RPC/JSON-RPC works; UI-only steps fall to browser"
    elif br_ok:
        tier, why = "browser", "API not authenticated — drive the web UI (needs login)"
    else:
        tier, why = "none", "no path available — set ODOO_* env or ODOO_SH_HOST"

    print(f"\n  → recommended tier: {GREEN if tier!='none' else RED}{tier}{END}  {DIM}({why}){END}")
    print(f"  {DIM}per-step overrides: SaaS Industry install → browser; custom-module deploy → ssh{END}\n")
    return 0 if tier != "none" else 1


if __name__ == "__main__":
    raise SystemExit(main())
