# MVP Build Brief — for building on Replit

Refined, build-ready plan for the app. Written so you (or Replit's AI agent) can build it in phases on
Replit. Assumes the **no-PHI MVP** (counts only, no patient names) — the fastest, lowest-liability path,
and the right call for a Replit build. Product name shown as `[PRODUCT]` until you pick one.

## Why this is a good fit for Replit
- The analytical core (`pipeline/engine.py`, `rates.py`, `selfcheck.py`) is **already written in Python**.
  A Replit **Python + Flask** app can import it directly — no rebuild of the math.
- Replit gives hosting, a URL, secrets management, and a built-in database — everything the MVP needs.
- Phases below are ordered so each one is **live and useful on its own** before you build the next.

---

## Phase 1 — Free Revenue Finder (build this first)
A hosted web app: practice enters five numbers → sees its headline uncaptured-revenue number → is asked
for contact info → gets a CTA to buy the full reviewed Blueprint / paid tier. This is your **lead engine**
and your first live product.

**Stack (Replit):** Python 3 · Flask · the existing `engine.py` (copied into the repl) · Replit DB or a
CSV for leads · email via Resend or SMTP (Gmail app password) to notify you of each lead.

**Screens:**
1. **Landing** — headline, "See your number free," credibility, sample link.
2. **Five-number form** — the existing intake fields (panel, % Medicare, % FFS, current CM, discharges).
3. **Lead gate** — Name · Practice · Email · Phone ("Where should we send your number?") *before* the result.
4. **Result** — big conservative headline number + 3 scenario ranges + "automated estimate" disclaimer +
   CTA ("Get your full reviewed analysis"). Emails the number to the practice and the lead to you.

**Data model (no PHI):**
```
Lead { name, practice, email, phone, panel_size, pct_medicare, pct_ffs,
       current_cm, discharges_month, headline_conservative, created_at }
```
No patient data, ever. Five practice-level numbers only.

**Reuse:** call `engine.run(Inputs(...))`, show only `scenarios.conservative.headline_uncaptured` + the
three scenario totals. Hold back everything else (that's the paid tier).

### Paste-into-Replit-AI-agent prompt (Phase 1)
> Build a Python Flask web app called [PRODUCT]. It has a landing page, a form collecting five numbers
> (active patient panel size, % Medicare, % traditional fee-for-service Medicare, patients currently
> billed monthly for care management, Medicare hospital discharges per month), then a contact gate
> (name, practice, email, phone), then a results page showing a single headline dollar figure and three
> scenario figures. Use the calculation module I'll paste (engine.py) — call engine.run() and display
> scenarios['conservative']['headline_uncaptured'] as the headline plus the moderate/optimistic totals.
> Store each submission (the five numbers + contact info + headline) in Replit DB, and email me a
> notification. Add a clear disclaimer that this is an automated estimate, not a reviewed analysis, and a
> call-to-action button linking to a checkout/contact page. Mobile-friendly, clean, no medical jargon.

## Phase 2 — Capture Playbook (the first paid tier)
Gated content that productizes the founder's expertise. Add simple **accounts** (Replit Auth or email
magic-link) and **Stripe** subscriptions. Behind the paywall:
- APCM/TCM/AWV eligibility rules, enrollment scripts, consent templates, monthly service-element checklists.
- Compliance guardrails (reuse `selfcheck.COMPLIANCE_REGISTRY`).
- Billing cheat-sheets + denial traps. Versioned and updated as CMS changes (the moat).

**Add to stack:** Stripe (subscriptions) · an auth method · a content store (Markdown files or a small DB).

## Phase 3 — Capture Dashboard (sticky, still no-PHI)
The practice enters **counts** (patients enrolled by APCM tier, AWVs done this year, TCMs billed) and sees:
- **Captured vs. potential** gauge ("$X of your $Y opportunity captured").
- Monthly billing checklist export.
- AWV-due and re-enrollment reminders (count-based, no patient names).

**Data model adds:**
```
Account { practice, plan, ... }
MonthlyLog { account_id, month, apcm_l1, apcm_l2, apcm_l3, awv_done, tcm_billed }
```
Still no PHI — the practice keeps patient names in their own EHR; the app tracks numbers.

---

## Pricing (confirmed in product-strategy.md)
Free Finder → **$199 Starter / $399 Practice / $899 Group** per month, flat. Annual ≈ 2 months free.
Wire Stripe products to these tiers in Phase 2.

## Build sequence & rough effort (on Replit)
1. **Phase 1 (Finder):** small — a few days. Live lead engine. **Start here.**
2. **Phase 2 (Playbook + Stripe + auth):** medium — the first revenue.
3. **Phase 3 (Dashboard):** medium — the stickiness.

## Guardrails carried from the consulting model
- No PHI in the MVP. Five practice-level numbers + counts only.
- The **$50k guarantee stays on the human-reviewed Blueprint only**, never the automated app tiers.
- Keep rates/rules current in one place (`rates.py` + compliance registry) so Finder, Playbook, and any
  reviewed Blueprint always agree.

## Still to decide
- **Product name** (see options provided separately) → replace `[PRODUCT]` everywhere + buy the domain.
- Confirm **no-PHI MVP** (assumed here).
- Whether to build Phase 1 yourself on Replit with its AI agent (using the prompt above) or have it built for you.
