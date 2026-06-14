# Casa Escondida Anilao — Strategy & Odoo 19 ERP Blueprint

Prepared by **Technext** for **Casa Escondida Anilao Resort & Dive Center** (casaescondida-anilao.com),
a PADI 5★ dive resort in Anilao/Mabini, Batangas, Philippines.

## Contents

| Path | What it is |
|------|------------|
| [`index.html`](index.html) | **The deliverable** — a single, self-contained, interactive report: client due-diligence, web/social research, PESTLE/SWOT/TOWS/Porter's, competitor & market analysis, valuation, stakeholder & 14 department workflows, AI/automation catalog, Odoo 19 architecture, implementation/change-management/hypercare plan, and a 5-lens consultant analysis. 27 sections, 40+ charts & diagrams. |
| [`odoo-build-spec/`](odoo-build-spec/) | Machine-readable, MCP-ready Odoo 19 build spec: modules, data model, demo data, automations, and the exact MCP execution runbook. |
| [`agents/`](agents/) | The multi-agent build loop (Orchestrator + stage agents) that executes the spec once an Odoo MCP server is connected. |

## View the report

Open `index.html` in any modern browser. It is fully self-contained (charts via Chart.js CDN,
diagrams via Mermaid CDN). Toggle dark/light, search sections, and print/export to PDF from the top bar.

## The "next step" (Odoo build)

No Odoo MCP server was connected when this was produced, so the Odoo instance is **not** built here.
The build is specified to be executed later:

1. Stand up an Odoo 19 instance and connect it via an Odoo MCP server.
2. Point an AI agent at [`odoo-build-spec/mcp-runbook.md`](odoo-build-spec/mcp-runbook.md).
3. Run the loop in [`agents/orchestration.md`](agents/orchestration.md) — it installs the top
   8–12 modules and loads the extensive demo dataset, gating each stage on a verification query.

## Notes

Figures labelled *estimate* (valuation, revenue, channel mix) are modelled planning assumptions, not
audited financials. The "Andrew" co-founder and exact staff roster are client-stated and were not
verifiable online — flagged accordingly in the report's appendix.
