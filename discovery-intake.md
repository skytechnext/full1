# Casa Escondida — Google Drive intake inventory (documented 20 Aug 2026)

Two parallel sets of **intake Google Forms**, one form per audience in each set — a short "quick one"
and a longer "when you have time". All owned by **jett@technext.asia**. Captured via the Drive API
(titles/owners/dates/links). **Form question & response text is NOT retrievable through the Drive API
or via the shared links** — see the limitation note.

## Set A — "quick one" — folder "Casa Escondida - intake (2026)"
- **Folder ID:** `1Pva-xUoU2TJiYJ8h6eAewEbSNCqQQco7` · created 13 Aug 2026
- **URL:** https://drive.google.com/drive/folders/1Pva-xUoU2TJiYJ8h6eAewEbSNCqQQco7

| Form | Audience | File ID | Size |
|---|---|---|---|
| Casa Escondida — the quick one, **for Andrew** | Owner/GM | `1I8ckYiL66zDKdfOdiEvboK0SsGpw71SuCeiJh-1Cr8E` | 2.3 KB |
| Casa Escondida — the quick one, **for Eloisa** | Front office / reservations | `1zDS4D5uOoq092BxH1PK-mNdofq87q4NimLxOwiMnQzA` | 1.0 KB |
| Casa Escondida — the quick one, **for the dive centre** | Dive ops | `1-pAqslp00nYj-cEZbs9zFpvEd1NeOh0sTDkQfkoyIaI` | 1.0 KB |
| Casa Escondida — the quick one, **for the kitchen and bar** | F&B | `1FqshB1HQEbsDb9RjE-RoFVY5owltE7g2IIqTP_ZWU0o` | 1.0 KB |

## Set B — "when you have time" — folder "Casa Escondida - intake, when you have time (2026)"
- **Folder ID:** `1PYA5oTC8AQJ0Di0I3q7VmZiYu7ol2Kuu` · created 15 Aug 2026
- **URL:** https://drive.google.com/drive/folders/1PYA5oTC8AQJ0Di0I3q7VmZiYu7ol2Kuu

| Form | Audience | File ID | Size |
|---|---|---|---|
| Casa Escondida — when you have time, **for Andrew & Dong** | Owners/GM & dive lead | `1AQNO_txVBFnU99Ugc_TQjyUZzkXgPtKlenvCb5G8Mb4` | 3.0 KB |
| Casa Escondida — when you have time, **for Eloisa** | Front office / reservations | `1ZDoQdP-i-LUNCe7Hsf8vDsm4MwV2SaxwHSemM3eL4eo` | 2.4 KB |
| Casa Escondida — when you have time, **for the dive centre** | Dive ops | `1E0LP1LidVXO-pi02WhKlxAC7Ru-Ez6zqwID9eJbg1Hk` | 1.0 KB |
| Casa Escondida — when you have time, **for the kitchen and bar** | F&B | `1GJgnZ8zJ9gf0dxFqfTK8bJKxjN0Qyr8N1t5WoSLwnOo` | 2.3 KB |

Structure: 4 audiences × 2 depths (quick / detailed) = 8 role-specific questionnaires gathering
department-level operational detail for the ERP build.

## Limitation — why the shared links don't let me read the questions
- The Drive API cannot export Google Forms content (`read_file_content` → unsupported mime type;
  `download_file_content` → internal error).
- The public `/viewform` and `/preview` pages return **HTTP 401** — the forms require Google sign-in,
  which my tools don't have (the edit/preview links open for the owner only).
- Link *format* is irrelevant (`?usp=…&ouid=…`, `/edit`, `/preview` all resolve to the same file ID).

### To get the questions & answers to me, pick one (best first):
1. **Responses → Sheets:** in each Form, Responses tab → the green **Sheets** icon → "Link to Sheets".
   Share the resulting spreadsheet. Header row = the questions, rows = answers. I read Sheets cleanly →
   full Q&A capture per department.
2. **Export to PDF:** Form → ⋮ → **Print → Save as PDF** → upload to Drive. Gives the questions (no answers).
3. **Copy questions into a Google Doc** and share it. I read Docs.

## Related Casa Escondida materials elsewhere in the Drive (not in these folders; readable on request)
Scoping Meeting 2 notes (Doc) + recording (MP4); `Casa_Escondida_Marketing_Proposal_TechNextAsia_2026.docx`;
`Casa Escondida Estimates.xlsx`; `Team Activities.xlsx`; various `index.html`/`CASA_Discovery.html`/
`Casa 5-Day Plan.html`/`changelog.html`; `dive_resort.py`.
