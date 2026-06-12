# The 7-Day Plan — Land the First Paid Blueprint

**Rule:** maximum one hour per day. This plan assumes everything in this repo is already built (it is).
Your only job this week is to put it in front of the right people and run it once.

**Targets for the week:** 5 messages sent → 1 intake call booked → 1 Blueprint delivered → 1 working
session held. That's the whole funnel.

---

## Day 1 — Customize and aim (≤ 60 min)
- Open `outreach/first-contact-messages.md`. Fill in real names and details for all five recipients.
- Cross off anyone who is an ADA-grant practice you serve directly. For message 5, confirm the PCP is
  **out of your home state**.
- Find email addresses (your old contacts, LinkedIn, practice websites, or the NPI registry for the
  practice's listed contact).
- Save each finished message as a draft. Do **not** send yet.
- **End-of-day deliverable:** five personalized drafts, five email addresses.

## Day 2 — Send the first batch + log (≤ 45 min)
- Send messages 1, 2, and 3 (your warmest relationships first).
- Start a simple log (a spreadsheet or the bottom of the messages file): recipient, date sent, status.
- **Deliverable:** three messages out, logged.

## Day 3 — Send the rest + first follow-ups (≤ 45 min)
- Send messages 4 and 5.
- Reply promptly to anyone who responded to Day 2. If someone's interested, propose two specific times
  for the 15-minute intake call this week.
- **Deliverable:** all five sent; at least one call time proposed.

## Day 4 — Intake call + load the pipeline (≤ 60 min)
- Run one 15-minute intake call. Gather the five numbers (use `intake/intake-form.html` on screen as your
  script, or fill it in live — it produces an `inputs.json` you can download).
- On the call, confirm two assumptions that move the number: their **current AWV completion** and whether
  they have a **reliable hospital discharge feed** (for TCM).
- Save the practice's numbers as `pipeline/inputs_<practice>.json` (copy the Westbrook file as a template).
- Run it:
  ```
  cd pipeline
  python3 generate.py inputs_<practice>.json
  ```
- **Deliverable:** a draft Blueprint PDF in `samples/` and a green self-check in your terminal.

## Day 5 — Review draft + run the gate (≤ 60 min)
- Read the draft Blueprint end to end. Sanity-check the headline against the practice's reality.
- Confirm the self-check printed **OVERALL GATE: PASS**. If any line said FAIL, fix the input/assumption
  and re-run — the pipeline will not render a PDF that fails the gate.
- **Before a paid send:** open `pipeline/rates.py`, verify each 2026 rate against your trusted source, and
  set `RATE_TABLE_STATUS = "VERIFIED"` with today's date. Re-run so the PDF shows VERIFIED, not provisional.
- Make any wording edits (the contact name, your firm name, their state).
- **Deliverable:** a final, gate-passed, rate-verified Blueprint PDF.

## Day 6 — Deliver with a cover email (≤ 45 min)
- Send the final Blueprint. Keep the cover email short:
  > Dr. [Name] — your Workflow Fit Blueprint is attached. The headline: about **$[conservative number]** in
  > new annual Medicare revenue you're not capturing today, conservatively. Pages 8–9 lay out three ways to
  > run it (in-house, turnkey, hybrid) with net revenue after cost, and a 90-day roadmap. Let's take 30
  > minutes this week to walk it and decide which path fits — does [day/time] work?
- Propose the Day 7 working-session time in this same email.
- **Deliverable:** Blueprint delivered; working session scheduled.

## Day 7 — Working session + decision gate (≤ 45 min)
- 30-minute session. Walk the headline, the three scenarios, and the three paths.
- Drive to one decision: **which path** (in-house / turnkey / hybrid) and **what the first step** is.
- Confirm the invoice. (Trial clients: $750 and the testimonial. Standard: $1,500.) If the conservative
  scenario didn't clear $50k, honor the guarantee — no charge — and ask for a referral instead.
- **Deliverable:** a paid (or guarantee-honored) engagement and a chosen path.

---

### If you only do one thing each day
| Day | The one thing |
|----|----------------|
| 1 | Personalize the five messages |
| 2 | Send three |
| 3 | Send two, propose a call time |
| 4 | Run one intake call, load the pipeline |
| 5 | Review the draft, verify rates, pass the gate |
| 6 | Deliver with a short cover email |
| 7 | Working session → path decision → invoice |

### Follow-up cadence (after Day 7)
Non-responders are normal. Send one short follow-up 3–4 business days after the original. One. Then leave
it — a second batch of five new names next week beats nagging the first five.
