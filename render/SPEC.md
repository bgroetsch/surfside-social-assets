# Brochure card spec

Open an issue in this repo titled `[render] <short description>` whose body is one JSON object (a ```json fence is fine). The "Render brochure card" workflow renders it with Chromium, commits the JPG at `path`, and comments `ASSET_READY` plus the GitHub Pages URL, or `ASSET_FAILED` plus the reason (for example text too long, a photo that won't load, a bad host). Open one issue at a time and wait for the reply.

```json
{
  "template": "f5",
  "scheme": "reverse",
  "path": "rental-cards/2026-10-28/rental-146522-f5-reverse.jpg",
  "card": { ... }
}
```

- `template`: `f1` bold banner, `f2` magazine, `f3` luxury full-bleed, `f4` collage, `f5` cream editorial, `f6` split panel, `f7` data sheet (land, commercial, or any property with few photos).
- `scheme`: `classic`, `reverse`, `midnight`, `harbor`.
- `path`: `remax-cards/<post date>/mls-<mls>-<template>-<scheme>.jpg` for sale listings, `rental-cards/<post date>/rental-<property id>-<template>-<scheme>.jpg` for vacation rentals. The template and scheme in the file name let the next run see what was used recently.

## card fields

All text is plain text (no HTML). Missing optional fields are simply left off the card. Never put a fact on a card that isn't in the source data.

| field | used for |
|---|---|
| `kind` | `"listing"` or `"rental"`. Rentals show a booking block instead of an agent. |
| `photos` | 1 to 4 image URLs. `photos[0]` is the hero (the primary exterior). `photos[1..3]` are insets, one per room. Hosts allowed: d36xftgacqn2p.cloudfront.net (MLS), d2td4dobkk213c.cloudfront.net (headshots), realtimerental.com (rental photos), bgroetsch.github.io. |
| `photo_labels` | Optional labels, same order as `photos` (e.g. `["", "Kitchen", "Living room"]`). Only label a room you have confirmed from the photo or the source data. |
| `hero_pos` | Optional CSS background-position for the hero, e.g. `"center 60%"`. |
| `badge` | Short headline tag: `JUST LISTED`, `PRICE IMPROVED`, `NEW PRICE!`, `2 FALL WEEKS OPEN`, `FEATURED RENTAL`. f1 and f4 show it very large, so keep it to about 3 words there. |
| `kicker` | Small location line, e.g. `NORTH CAPE MAY · BAYSIDE`. |
| `headline` | Street address for listings; property name or address for rentals. |
| `headline_tail` | f7 only: lighter words after the headline, e.g. `ON 1.07 ACRES`. |
| `address` | f7 only: bottom-left address if the headline is not the address. |
| `subline` | Town line, e.g. `North Cape May, NJ`. |
| `tagline` | One short descriptive line (f2, f3, f4, f5). |
| `price` | Listings: list price. Rentals: a confirmed weekly rate for an open week only, otherwise omit. |
| `price_label` | e.g. `ASKING`, `PER WEEK`. |
| `price_suffix` | f7 only, e.g. `PER LOT`. |
| `price_note` | f5: up to 3 short lines next to the price (use `\n`). |
| `stats` | `[["3","BEDROOMS"],["2.5","BATHS"],["2,033","SQ FT"]]`. Up to 4 (f5 shows 3). Use `SLEEPS` for rentals. |
| `rows` | f7: up to 4 `[label, value]` rows. Defaults to stats. |
| `bullets` | f1: up to 5 short lines. Defaults to stats. |
| `chips` | f4: up to 4 short pills. Defaults to stats. |
| `star` | f1: optional 1-2 word starburst (`OCEAN\nVIEW`, `POOL`). Omit unless true. |
| `panel` | f7: `{"big": "2", "text": "LOTS\nAVAILABLE"}` when there aren't 2 inset photos. |
| `note_box` | f7: `{"label": "Minutes to", "text": "..."}` filler box when there aren't 2 inset photos. |
| `agents` | Listings: `[{"name","phone","email","headshot"}]`. First agent's phone and email are shown. Add a second agent only if they are with REMAX Surfside. Leave `headshot` off when the agent's headshot doesn't meet the minimum. |
| `booking` | Rentals (optional): `{"label": "BOOK YOUR STAY", "site": "SurfsideCapeMay.com", "note": "Photos, rates & live calendar"}`. These are the defaults. |

Every card automatically carries the REMAX Surfside lighthouse logo, office address, "Each Office Independently Owned and Operated" and the office phone 609-884-4242 at 42px. The renderer refuses any card where an agent phone is not smaller than the office phone.

## Choosing a format and scheme

- Land and commercial: f7. Anything with fewer than 3 usable photos: f7 or f3.
- Otherwise rotate f1 to f6 and the four schemes so the page doesn't repeat a look. Before picking, read the card file names on this week's Buffer posts for the REMAX SURFSIDE Facebook channel (both listings and rentals) and avoid any format or scheme used by the post immediately before or after on the calendar. Never repeat an exact format + scheme pair used in the last 3 weeks of that stream's posting history.
