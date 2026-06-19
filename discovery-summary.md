# Discovery & Requirements Summary — Casa Escondida × Technext

**Updated from the kick-off/scoping meeting, 11 Jun 2026** (Andrew Oh + resort team; Dong absent).
This supersedes pre-discovery assumptions in earlier drafts of the report.

## Principals & roles
- **Andrew Oh** (andrew.oh@spur.com.sg) — co-founder, Singaporean businessman (also owns a telecom company),
  PADI instructor. Owns **overseas guest relations, marketing, kitchen/restaurant**. Final decision-maker.
  Philosophy: *"80% preparation, 20% execution."* **#1 priority: stop cash leakage from overspending.**
- **Dong (Armando Vergara)** — co-founder, heads **dive center + maintenance**, approves petty cash,
  sets instructor/weekend priority. Final decision-maker. Did not attend; PADI ratings to be confirmed.
- **Ms. Eloisa** — **Reservations & Marketing Manager**; runs the whole booking lifecycle manually across
  email/FB/WhatsApp/Viber/IG; aligns rates by hand; handles deposits, DOT reports, IDs, transfers.

## Key facts captured (corrections to earlier assumptions)
| Topic | Finding |
|---|---|
| Rooms | **24** per meeting (16 Standard no-view + 4 Deluxe + 4 Suite); **official 2026 rate card lists 23** (15 Standard + 2 Deluxe + 2 White Beach Deluxe + 4 Suite). Only **8 are sea-view**. |
| Staff | **36 regular** (admin, maintenance, security, drivers, housekeeping, kitchen & dining, dive center) + 6–10 extras. |
| Pricing | **Flat annual** rates (Jan applies all year); no early-bird/last-minute. Discounts: repeat ≤10%, agents 20% (net pricing), instructors 10%. |
| Channels | Mostly **direct** (80–90% repeat, mostly local). **Booking.com only ~15%, capped, closed weekends**. No channel manager. Booking.com remits in 8–9 days. |
| Payments | Cash, credit card, **GCash**, bank transfer (WeChat noted). Quote/accept now in **PHP** (was USD). |
| Accounting | In-house "accounts club", no full-time accountant; Andrew lent his telecom-company corporate accountant. Books were "a big mess" (expenses, commissions, VAT). |
| POS / BIR | Internal non-commercial DB since 2021; old POS **was** BIR-accredited but lapsed; current is **NOT** BIR-accredited (legal gap). |
| Deposits | 50% deposit (direct); Booking.com collects full. No refunds; rebook ≥7 days; no-show forfeits 50%. |
| Billing | Consolidated at checkout; group or individual; no service charge; tipping culture (3 tip boxes — Andrew wants to revise). |
| Budgeting | Per-guest ("per pack"), ~₱1,000/guest buffet, keep 20-pack inventory, FIFO. Dive shop: only diesel for compressors. |
| Markets | China (via HK), Taiwan, HK, Singapore, Asia; Europe future. Overseas fill weekdays; locals weekends. Season Jan–Jun. |
| Compliance | DOT-accredited; submits guest-arrival reports; stores passports/IDs in a "GC" folder. |
| Devices | **3 POS units** to start (dive shop priority), **shared departmental logins**, non-waterproof. |
| Critical pain | Broken, unaccountable **communication** first-contact → dive team/kitchen (group chats). A guest once went un-attended. |

## Aligned decisions
- Website + chatbot in **English + Simplified + Traditional Chinese**; correct **Chinese brand name**; no JP/KR.
- **AI chatbot** across Facebook, WhatsApp, Viber (+ web) for lead capture, translation, next-day approval.
- **3 POS units, shared departmental accounts.**
- **Phased rollout — Phase 1 = POS + Inventory**, then accounting/GL, then the rest.
- **Andrew & Dong = final decision-makers.**

## Client-instructed additions (this round)
- **PMS:** use **Webkul** paid Hotel/PMS module.
- **Channel manager:** **QloApps** + `hotel_qloapps_channel_manager` (Odoo connector; needs QloApps subscription).
- **Build target:** `edu-escondida.odoo.com` — **delete old demo items first**, then generate fresh demo
  (pictures, items, text, entries). Token supplied out-of-band — **kept out of the repo** (see `odoo-build-spec/instance.md`).
- Research modern/beginner dive services, innovative dive gear, dive-shop AI daily briefing, owner growth
  decisions, top-3 competitor deep-dive (incl. Solitude Acacia), new personas, BPMN/blueprint/UML — all added to `index.html`.

## Open follow-ups (owner to provide)
- Dong's PADI ratings/member number; instructor cert list & expiries.
- Agent rate sheet, room+dive "shopping list", sample quotation, guest-profile data sample.
- Full accounting pack + BIR details + floor plan + WiFi/network map (see `stakeholder-questions.html`).
- Confirm exact room count (23 vs 24) and sea-view mapping.
- Chatbot FAQs; Chinese brand name & assets; website dry-run feedback.

## Scheduling
Andrew back **21 Jun**, available ~21–27; soft on-site week of **22–26 Jul**, formal implementation in July.
No fixed go-live date (Andrew: systems must be tested/improved over time).

---

## Scoping Meeting 2 — 18 Jun 2026 (updates & corrections)
Attendees: **Dong** (joined from Batangas, travelling next day) + **Ms. Eloisa**; TechNext (RJ, Pia, Phillip=lead dev, Jett=functional consultant, Rico=web/marketing, Sky=strategy, +VN/SG team). **Andrew was not on the call** (in Singapore meeting Sky; he is the primary client contact and is upskilling in AI — new MacBook with Claude).

**New / changed vs Meeting 1**
- **Rooms: 24, of which 8 are ocean-view** (16 Standard no-view + 2 Deluxe + 2 White Beach Deluxe + 4 Suite). (Supersedes the 23 figure.)
- **Breakfast is optional** — website's “breakfast included / 100%” is wrong; change to optional.
- **Remove Booking.com from the website** — its data is “not accurate anymore”; focus reviews on **TripAdvisor + Google**.
- **“24/7 front office” claim is false** — to be removed from the website.
- **Owner = Edwin/Evan** (CEO-level) surfaced; an owner-level meeting (Edwin + Dong) is a next step. Dong is “more like a resort manager” who **guides self-managing department heads**.
- **Dive ratio confirmed 6:1** (+ safety diver beyond six).
- **~90% of guests are divers**; new website already produced **3 enquiries in week 1**.

**Requirements reinforced/new**
- Odoo all-in-one (Accounting, POS, Inventory, Purchasing, Diving) — confirmed.
- **Single folio**, settled at checkout; **charge to a room OR a person** (rooms are sometimes shared).
- **Automated dive-crew scheduling**: any booking door → DM schedule + notification (avoid forcing an app download — push a message instead).
- **Digital rental waiver/signature in POS** (gear-rental disputes: guests deny renting → lost revenue).
- **POS prices editable** via Odoo Inventory.
- AI chatbot + social management (Messenger + email unified, offline lead capture); AI videos/motion graphics for IG/FB (Rico); Chinese translation live, Chinese brand name “under Andrew”.
- **Success metric (6 months, Dong):** “reduce repeat mistakes… make everything faster.”

**Infra / data**
- Computers only in the office (desktops); all other staff use **personal phones**. Internet stable with **Starlink backup** (“it never stops”), incl. on-boat.
- Current **POS is the source of customer data** for migration and is **“too slow”** (manual workarounds).
- Cancellation: no refund; rebook for weather/medical; **no-show forfeits 50% deposit** (implies 50% deposit).
- Dive package includes boat, 1 DM, tanks, dive permit; free snacks/drinks on boat; special meals charged to room.
- Decompression chamber ~1.5 h away (Batangas City); boats carry O2.

**Next steps**: client sends ~20–30 website change items via Eloisa → TechNext implements immediately; remove Booking.com + breakfast-optional (Rico); phases meeting (Sky/Andrew/Dong); owner meeting (Sky/Edwin/Dong); identify current-POS main user for Jett; comms via **WhatsApp**.

**Not discussed in Mtg 2** (still open): channel manager, BIR/CAS accreditation, payroll, kitchen-display, contract/commercials/budget, go-live date, edu-escondida.odoo.com.
