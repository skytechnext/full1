# Casa Escondida — Google Drive intake inventory (documented 20 Aug 2026)

Documentation of the two Drive folders provided by the client. Captured via the Drive API
(titles, owners, dates, links). **Google Forms question/answer content is not retrievable through
the Drive API** — see the limitation note below.

## Folder 1 — "Casa Escondida - intake, when you have time (2026)"
- **ID:** `1PYA5oTC8AQJ0Di0I3q7VmZiYu7ol2Kuu` · owner **jett@technext.asia** · created 15 Aug 2026
- **URL:** https://drive.google.com/drive/folders/1PYA5oTC8AQJ0Di0I3q7VmZiYu7ol2Kuu
- **Contents:** 4 role-specific intake **Google Forms** ("when you have time" questionnaires) — one per
  department/stakeholder, to gather operational detail for the ERP build. Response content not yet
  extractable (see below).

| Form (title) | Audience / purpose | File ID | Created | Approx. size |
|---|---|---|---|---|
| Casa Escondida — when you have time, **for Andrew & Dong** | Owners / GM & dive lead — leadership & cross-ops | `1AQNO_txVBFnU99Ugc_TQjyUZzkXgPtKlenvCb5G8Mb4` | 15 Aug 2026 | 3.0 KB (largest) |
| Casa Escondida — when you have time, **for Eloisa** | Ms. Eloisa — front office / reservations | `1ZDoQdP-i-LUNCe7Hsf8vDsm4MwV2SaxwHSemM3eL4eo` | 15 Aug 2026 | 2.4 KB |
| Casa Escondida — when you have time, **for the kitchen and bar** | Restaurant & bar / F&B | `1GJgnZ8zJ9gf0dxFqfTK8bJKxjN0Qyr8N1t5WoSLwnOo` | 15 Aug 2026 | 2.3 KB |
| Casa Escondida — when you have time, **for the dive centre** | Dive operations | `1E0LP1LidVXO-pi02WhKlxAC7Ru-Ez6zqwID9eJbg1Hk` | 15 Aug 2026 | 1.0 KB (smallest) |

Form edit links:
- Andrew & Dong — https://docs.google.com/forms/d/1AQNO_txVBFnU99Ugc_TQjyUZzkXgPtKlenvCb5G8Mb4/edit
- Eloisa — https://docs.google.com/forms/d/1ZDoQdP-i-LUNCe7Hsf8vDsm4MwV2SaxwHSemM3eL4eo/edit
- Kitchen & bar — https://docs.google.com/forms/d/1GJgnZ8zJ9gf0dxFqfTK8bJKxjN0Qyr8N1t5WoSLwnOo/edit
- Dive centre — https://docs.google.com/forms/d/1E0LP1LidVXO-pi02WhKlxAC7Ru-Ez6zqwID9eJbg1Hk/edit

## Folder 2 — "Casa Escondida - intake (2026)"
- **ID:** `1Pva-xUoU2TJiYJ8h6eAewEbSNCqQQco7` · owner **jett@technext.asia** · created 13 Aug 2026 · shared 20 Aug 2026
- **URL:** https://drive.google.com/drive/folders/1Pva-xUoU2TJiYJ8h6eAewEbSNCqQQco7
- **Contents:** **empty** at time of documentation (no files accessible under this parent). Likely the
  destination for collected intake responses / materials once submitted.

## Limitation — extracting the Forms' actual questions & answers
The Drive API cannot export Google Forms content (`read_file_content` → unsupported mime type;
`download_file_content` → internal error). To document the real questions and any responses, do ONE of:
1. In each Form → **Responses → link to Sheets** (creates a responses spreadsheet), then share the
   sheet — it reads cleanly and I can document questions + answers.
2. Or **File → Download / print each Form** and share as PDF/Doc.
3. Or grant Forms-API access.
Once any of those is available, this inventory can be expanded into a full Q&A capture per department.

## Related Casa Escondida materials seen elsewhere in the Drive (NOT in the two folders above)
Surfaced by search; readable if you want them documented too (say the word):
- *Casa Escondida x TechNext — Scoping Meeting 2 (18 Jun 2026) — Notes by Gemini* (Google Doc) + recording (MP4)
- *Casa_Escondida_Marketing_Proposal_TechNextAsia_2026.docx*
- *Casa Escondida Estimates.xlsx* · *Team Activities.xlsx*
- Various `index.html` / `CASA_Discovery.html` / `Casa 5-Day Plan.html` / `changelog.html` and `dive_resort.py`
