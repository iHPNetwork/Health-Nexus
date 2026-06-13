# Workflow Fit Blueprint — Operating Kit

A complete, self-contained operation for a single-operator healthcare revenue-consulting business. It
turns five practice-level numbers into a professional 10–12 page PDF that shows a primary care practice
its uncaptured annual Medicare care-management revenue, the models that fit its workflow, three
implementation paths with honest net revenue, a 90-day roadmap, compliance guardrails, and staff scripts.

**The offer:** $1,500 per Blueprint ($750 for the first five clients, for testimonials).
**The guarantee:** if the conservative scenario doesn't identify $50k+ in new annual revenue, the client
doesn't pay.

---

## What's in here

| Path | What it is |
|------|------------|
| `landing/index.html` | The landing page. Plain, professional, no hype. The front door. |
| `intake/intake-form.html` | The five-number intake form. Validates input, outputs `inputs.json`. |
| `pipeline/rates.py` | **Master rate table** — the single source of truth for every dollar figure. |
| `pipeline/engine.py` | Calculation engine: five numbers → three scenarios across APCM, TCM, AWV. |
| `pipeline/selfcheck.py` | **The self-check gate** — independently recomputes everything; pass/fail. |
| `pipeline/blueprint.py` | Renders the Blueprint to print-ready HTML. |
| `pipeline/generate.py` | The pipeline entry point. Runs the gate, then renders HTML + PDF. |
| `pipeline/inputs_westbrook.json` | Sample inputs for the demo practice. |
| `samples/westbrook-family-medicine.pdf` | **The finished sample Blueprint** (lead magnet / proof). |
| `outreach/first-contact-messages.md` | Five personalized first-contact messages. |
| `plan/7-day-plan.md` | Day-by-day plan (≤ 1 hr/day) to land the first paid job. |

---

## Quick start

### Generate a Blueprint
```bash
cd pipeline
python3 generate.py inputs_westbrook.json      # uses the included sample
# or, for a real client:
python3 generate.py inputs_<practice>.json      # your own JSON, same schema
python3 generate.py --demo                       # rebuild the Westbrook sample
```
Output lands in `samples/<practice-slug>.html` and `.pdf`. The console prints the full self-check report.

**The gate is enforced:** if the self-check fails, no PDF is written. Fix the flagged issue and re-run.

### Input JSON schema (the five numbers + labels)
```json
{
  "practice_name": "Westbrook Family Medicine",
  "prepared_for": "Dr. [Practice Lead]",
  "prepared_by": "Campbell3, LLC",
  "state": "[State]",
  "physicians": 4,
  "panel_size": 7500,
  "pct_medicare": 28,
  "pct_ffs_of_medicare": 65,
  "current_cm_patients": 60,
  "medicare_discharges_month": 40
}
```
The intake form produces exactly this file — fill it in on a call, download `inputs.json`, run the pipeline.

---

## ⚠️ Before your first PAID client — verify the rates (5 minutes)

The dollar values in `pipeline/rates.py` are **conservative 2026 estimates** and are flagged
`PROVISIONAL`. The Blueprint will render and the self-check will pass so you can practice, but every PDF
carries a visible "RATES PROVISIONAL" badge until you confirm them.

1. Open `pipeline/rates.py`.
2. Check each value in `RATES` against your trusted 2026 source (the CMS 2026 PFS final rule or your
   verified sample Blueprint).
3. Set `RATE_TABLE_STATUS = "VERIFIED"` and `RATE_TABLE_VERIFIED_DATE = "YYYY-MM-DD"`.
4. Re-run. The badge now reads `VERIFIED`.

This is the one piece that requires your judgment. Everything else runs itself.

---

## The self-check gate (what it guarantees)

Before any PDF renders, `selfcheck.py` independently re-derives every figure (separate code path from the
engine) and confirms:

1. **All arithmetic recomputed independently** and reconciled to the engine, per scenario.
2. **Every rate is registered** in the master table — no orphan/improvised numbers can reach a calculation.
3. **No double-counting** — APCM *replaces* CCM, so existing care-management billing is subtracted, never added.
4. **Mixes sum to 1.0** — no leaked or invented patients in the tier/complexity/AWV splits.
5. **The $50k guarantee threshold** is evaluated against the **conservative** scenario.
6. **The headline = APCM (net of existing) + TCM + AWV** — exactly, or the gate fails.
7. **Every compliance statement** carries a registered CMS basis before it can print.
8. **Sanity bounds** — no negative revenue, enrolled ≤ eligible, scenarios monotonic.

If anything fails, the pipeline refuses to render. *If a number can't be verified, it's removed, not softened.*

---

## How the numbers are built (plain version)

- **APCM** — eligible traditional FFS Medicare patients × enrollment rate, split across the three APCM
  tiers, annualized, then reduced by the care management the practice already bills.
- **TCM** — annual Medicare discharges × capture rate, split moderate/high complexity.
- **AWV** — eligible FFS Medicare × the gain from assumed current completion up to the scenario target.
- **Three scenarios** (conservative / moderate / optimistic) differ only in adoption assumptions; same
  rates, same eligibility. Conservative is deliberately low — the number to build a decision on.
- **Three operational paths** (in-house / turnkey / hybrid) show net revenue after realistic cost, using
  the conservative APCM gross as a floor.

All assumptions live, clearly labeled and editable, in `pipeline/rates.py`.

---

## Wiring the forms to a backend (optional, later)

Both HTML files are fully standalone and need no server to demo. Neither submits to a backend in this
build (single-operator, zero-maintenance by design):
- **Intake form** shows the captured JSON and offers it as an `inputs.json` download.
- **Landing form** confirms the lead on screen.

When you want submissions delivered automatically, point either form's submit handler at a no-code form
service (Formspree, Google Forms, a Zapier webhook) — a one-line change in the inline `<script>`.

---

## Running on Replit

1. **Create Repl → Import from GitHub** and paste this repo's URL.
2. Replit reads `replit.nix` (system libraries for WeasyPrint) and `requirements.txt` (the
   `weasyprint` package) automatically.
3. Press **Run**. `server.py` starts and Replit gives you a live URL:
   - `/` — the landing page (this is the shareable link for outreach)
   - `/intake` — the intake form
   - `/sample` — the sample Blueprint
4. To **generate a Blueprint**, open the Replit **Shell** and run:
   ```
   cd pipeline && python3 generate.py inputs_westbrook.json
   ```

If PDF rendering ever fails on Replit (a missing system library), the pipeline still writes
the HTML — open it and Print → Save as PDF. Everything else runs unchanged.

## Dependencies

- **Python 3.9+** with **WeasyPrint** (`pip install weasyprint`) for PDF rendering. If WeasyPrint isn't
  available, the pipeline still writes the HTML — open it and Print → Save as PDF as a fallback.
- The HTML files need nothing — open them in any browser.

---

## Guardrails baked in

- **No PHI** anywhere — five practice-level numbers only.
- **Conservative by default** — the guarantee is real, so the headline is the conservative figure.
- **Moonlighting-safe** — nothing here touches DPP coverage, health-plan negotiation, or employer group
  sales. Don't run a Blueprint for a practice you serve through the ADA grant.
