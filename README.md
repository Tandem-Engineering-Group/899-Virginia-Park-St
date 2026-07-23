# 899 Virginia Park St — Freeze/Water Damage Claim Workspace

Working repository for Jeff Stamm's Liberty Mutual claim **061004792**
(freeze event 02/26/2026 — boiler + radiators froze, water damage across 4 levels)
at 899 Virginia Park St, Detroit MI 48202.

> ⚠️ This repository contains personal insurance information and interior photos.
> Keep visibility restricted to the people working on the claim.

## 📍 The Photo Map portal

**`portal/index.html`** — open it in any browser (double-click from a local clone).
Every pack-out photo the insurance company took is pinned on the house floor plans with an
AI-generated description, room guess, and approximate contents value. Pins are draggable —
corrections save in the browser and can be exported/imported as JSON, or dumped to CSV.
See [portal/README - How to use the Photo Map.md](<portal/README - How to use the Photo Map.md>).

## Folder map

| Folder / file | Contents |
|---|---|
| `portal/` | The photo-map portal (self-contained: floor plans, thumbnails, analysis data) |
| `899 VP - JEFF - Insurance Photos/` | Original pack-out photos from the carrier (HEIC + PNG pairs, taken 3/15/2026) |
| `Stamm_Claim_061004792/` | Extracted claim package: master workbook, 401 line items CSV, payment letter, HVACi report, estimate summary |
| `001 Previous info/` | Earlier estimate-validation work (RSMeans workbooks, claim strategy report) |
| `Stamm Contractor Estimate.pdf` | 36-page detailed line-item structure estimate (includes the floor-plan sketches) |
| `Stamm Estimate.pdf` | ConRest agreed-price rollup + settlement math |
| `Stamm HVACi Report.pdf` | HVACi boiler/radiator assessment ($30,875.41 replacement scope) |

## Claim headline numbers (as of 07/2026)

- Replacement Cost Value: **$179,578.08**
- Recoverable depreciation held back: **$26,641.23**
- Supplemental payment 07/10/2026: **$116,884.57** · prior payments $31,052.28 · deductible $5,000
- ALE / loss-of-rent coverage runs to **December 18, 2026**

## Notes

- Photo locations and item values in the portal are **AI estimates** — starting points for the
  rebuild walkthrough, not appraisals.
- All 100 pack-out photos were shot in one ~10-minute walkthrough (1:15–1:26 PM, 3/15/2026),
  so photo-number order ≈ the crew's path through the house.
