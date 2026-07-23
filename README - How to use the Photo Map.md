# 899 Virginia Park — Pack-Out Photo Map

A local, offline "portal" that puts every insurance pack-out photo on the house floor plans,
with an AI-generated description, room guess, and approximate contents value for each photo.

## How to open it

Double-click **`index.html`** in this folder (opens in Edge or Chrome). Nothing is uploaded
anywhere — everything runs from this folder on your machine.

## What you're looking at

- **Floor tabs** (1st / 2nd / 3rd / Basement / Unplaced) — each shows the insurance floor-plan
  sketch from the Liberty Mutual estimate with numbered pins. The pin number is the photo number
  (pin `2478` = `IMG_2478`).
- **Pin colors**: green = analysis is fairly sure of the room · amber = approximate ·
  red = uncertain · **blue = you confirmed it**.
- **Drag a pin** to the exact spot the photo was taken. It saves automatically and turns blue.
- **Click a pin** (or a card in the right-hand list) to see the photo, what's in it, the estimated
  replacement value of each item, the clues used to guess the room, and any damage notes.
  Arrow keys move to the previous/next photo in the walkthrough. Click the photo to open the
  full-resolution original.
- **Unplaced tab**: photos the analysis couldn't put on a floor. Pick a floor from the dropdown,
  then drag the pin into position.
- In the photo panel you can **move a photo to a different floor/room**, **mark the location
  confirmed**, and add a **note for the rebuild** (e.g. "this mirror hung above the fireplace").

## Saving / sharing your corrections

Your dragging, confirmations, and notes are stored by the browser on this PC. Use the header buttons:

- **Export JSON** — saves all placements + notes to a file (back this up / send it around).
- **Import** — loads a placements file back in (e.g. on another PC).
- **CSV** — full photo inventory (file, room, items, value range, notes) for Excel.
- **Reset to AI** — throws away your manual changes and returns to the AI suggestions.

## Caveats

- Room locations and values are **AI estimates from the photos alone** — use them as a starting
  point, not as an appraisal. Values are rough used-replacement ranges, not insurance valuations.
- The walkthrough order helped locate photos: all 100 were taken in one ~10-minute pass on
  3/15/2026, so neighboring photo numbers are usually in the same room.

## Folder contents

- `index.html` — the portal (everything runs in here)
- `data.js` — the analysis results (photo → room, items, values)
- `plans/` — floor-plan images extracted from "Stamm Contractor Estimate.pdf"
- `thumbs/`, `mid/` — resized copies of the photos for fast browsing
  (originals stay untouched in `899 VP - JEFF - Insurance Photos`)
