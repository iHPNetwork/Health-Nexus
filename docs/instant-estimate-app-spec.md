# Instant Estimate App — design spec (phase two)

**Status:** plan only. Do **not** build until outreach is bringing steady traffic to the site (enough
that a free estimate would capture real volume). Right now, effort is better spent landing the first
1–3 paying clients. This doc is the blueprint for when that day comes.

## Purpose & positioning
A free, self-serve **lead magnet** — not a product you sell. A practice enters five numbers and instantly
sees their **headline uncaptured-revenue number**. That number creates the pull to buy the real thing:
the human-reviewed **$1,500 Practice Revenue Blueprint** (with the $50k guarantee).

- **Free tier = the hook.** Costs the practice nothing to learn they're leaving six figures on the table.
- **Paid tier = unchanged.** The $1,500 reviewed Blueprint and the guarantee stay exactly as they are.
- The free number **anchors** the $1,500 as the obvious next step.

## The funnel (screen flow)
```
1. Landing page  ──►  "See your number free" button
2. Five-number form  (the existing intake fields)
3. Lead capture gate  ──►  Name · Practice · Email · Phone   ("Where should we send your number?")
4. Instant result screen:
      • Big headline number (conservative)         ← shown
      • Conservative / Moderate / Optimistic range ← shown (ranges only)
      • "This is an automated estimate" disclaimer
      • CTA:  "Get your full reviewed Blueprint — $1,500, $50k guarantee"  ──► order
5. Auto-email to the practice (their number) + auto-email to Denise (the lead + their 5 numbers)
```
Put the lead-capture gate (step 3) **before** revealing the number — that's what turns a curious visitor
into a contact you can follow up with even if they don't buy on the spot.

## What the free tier SHOWS vs. HOLDS BACK
| Shown (free) | Held back (paid $1,500 Blueprint) |
|---|---|
| Headline uncaptured number (conservative) | Full 12-page report |
| The 3 scenario totals (ranges only) | Per-code breakdown (APCM tiers, TCM, AWV tables) |
| One-line "what's driving it" (e.g. "mostly APCM") | Three implementation paths + net revenue after cost |
| "Automated estimate" disclaimer | 90-day roadmap, compliance guardrails, staff scripts |
| CTA to buy the reviewed Blueprint | **The $50k guarantee** (only on the reviewed product) |

The free tier is deliberately *incomplete* — enough to create desire, not enough to act on. No guarantee
attaches to an unreviewed number.

## You already have the hard part
The calculation engine (`pipeline/engine.py`) already turns five numbers into the scenarios. The app is
just a thin web layer that calls it and shows **only the headline**. No new math, no new rate logic —
it reuses the exact same source of truth, so the free estimate and the paid Blueprint always agree.

## Build approach (when the time comes)
- **Thin serverless function** (e.g. Vercel/Netlify Function or a small FastAPI app) that imports the
  existing `engine.py`, returns the headline + ranges as JSON. The form posts to it; the result screen
  renders the number.
- **No database needed** to start — email the lead to Denise (same as the intake form does now) and store
  in a simple sheet/CRM.
- **Hosting cost:** roughly $0–20/month at low volume (serverless free tiers cover early traffic).
- **Effort:** ~1–2 days of build on top of what exists, because the engine is done.

## Guardrails (keep it honest)
- Label the free number clearly: **"Automated estimate based on five practice-level inputs. Not a
  reviewed analysis. No guarantee applies to this estimate."**
- No PHI — same five practice-level numbers as today.
- The **$50k guarantee never appears on the free tier** — it belongs only to the reviewed Blueprint.
- Keep the conservative figure as the headline (same conservative-by-default principle as the Blueprint).

## Pricing recap (decided)
- **Free** — instant estimate (this app). The lead magnet.
- **$1,500** — human-reviewed Blueprint + $50k guarantee. The flagship (unchanged).
- *(Optional later)* **$199** — automated full PDF as a tripwire, clearly "not individually reviewed," no
  guarantee. Only if you want to monetize self-serve directly; don't price it near $1,500.

## When to pull the trigger to build
Build the instant-estimate app once **either** is true:
1. Your site is getting enough visitors that a free estimate would capture meaningful leads each week, or
2. You're spending too much time hand-running estimates for tire-kickers who aren't ready to pay.

Until then: outreach → reviewed Blueprints → testimonials. The app is the scale lever, not the starter.
