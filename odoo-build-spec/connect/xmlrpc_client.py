"""Minimal, dependency-free Odoo XML-RPC client (Tier 2 / MCP fallback).

Reads connection details from environment variables so **no secret is ever committed**:

    ODOO_URL      e.g. https://edu-escondida.odoo.com
    ODOO_DB       database name
    ODOO_LOGIN    user email/login
    ODOO_API_KEY  API key (Settings -> Account Security -> New API Key) or password

Usage:
    from connect.xmlrpc_client import Odoo
    odoo = Odoo.from_env()
    odoo.x('res.partner', 'search_read', [[['customer_rank', '>', 0]]], {'fields': ['name'], 'limit': 5})

This is the same `x(model, method, args, kw)` helper pattern used throughout the build. Server-side
(Odoo.sh SSH, Tier 1) is preferred for bulk work and for methods that return void (which can fail
XML-RPC response marshalling even though they execute) — see connection.md.
"""

import os
import ssl
import xmlrpc.client


class Odoo:
    def __init__(self, url, db, login, api_key, insecure=False):
        if not all([url, db, login, api_key]):
            raise ValueError("Missing connection details — set ODOO_URL/ODOO_DB/ODOO_LOGIN/ODOO_API_KEY.")
        self.url = url.rstrip("/")
        self.db = db
        self.login = login
        self.api_key = api_key
        ctx = ssl._create_unverified_context() if insecure else None
        self._common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common", context=ctx)
        self._object = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object", context=ctx)
        self.uid = None

    @classmethod
    def from_env(cls):
        return cls(
            os.environ.get("ODOO_URL"),
            os.environ.get("ODOO_DB"),
            os.environ.get("ODOO_LOGIN"),
            os.environ.get("ODOO_API_KEY"),
            insecure=os.environ.get("ODOO_INSECURE") == "1",
        )

    def authenticate(self):
        self.uid = self._common.authenticate(self.db, self.login, self.api_key, {})
        if not self.uid:
            raise PermissionError("Authentication failed — check ODOO_DB/ODOO_LOGIN/ODOO_API_KEY.")
        return self.uid

    def version(self):
        return self._common.version()

    def x(self, model, method, args=None, kw=None):
        """execute_kw wrapper. args is a list of positional args; kw a dict of keyword args."""
        if self.uid is None:
            self.authenticate()
        return self._object.execute_kw(self.db, self.uid, self.api_key, model, method, args or [], kw or {})

    # convenience helpers
    def search_read(self, model, domain=None, fields=None, limit=None):
        kw = {"fields": fields or []}
        if limit:
            kw["limit"] = limit
        return self.x(model, "search_read", [domain or []], kw)

    def count(self, model, domain=None):
        return self.x(model, "search_count", [domain or []])

    def create(self, model, values):
        return self.x(model, "create", [values])

    def write(self, model, ids, values):
        return self.x(model, "write", [ids, values])


if __name__ == "__main__":
    o = Odoo.from_env()
    o.authenticate()
    print("Connected uid:", o.uid)
    print("Version:", o.version().get("server_version"))
    print("Installed modules:", o.count("ir.module.module", [["state", "=", "installed"]]))
