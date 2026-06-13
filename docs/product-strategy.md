# Product Strategy — pivoting the Blueprint into an app primary care practices love

**Context for the pivot:** the founder (Denise Campbell, Ph.D., MSPH) cannot operate as a visible personal
consultant alongside her ADA role, so the business must become a **self-serve software product** branded
as a company (Campbell3), not a personal consulting service. This document defines what that product
should be, why practices would pay for it, and at what price — grounded in 2025–2026 market research.

> Legal note (founder to confirm, not a build question): owning/operating a software company is still an
> "outside activity." Confirm it's permitted under whatever governs the ADA role. The subject-matter lane
> (practice-side primary care revenue) remains separate from payer/DPP/employer work.

---

## 1. The pain points (researched, not guessed)

| Pain | Evidence |
|---|---|
| **Money left on the table** | Small primary care practices leave **$73K–$468K/year** uncaptured from documentation/billing gaps — missed AWVs, CCM, TCM, modifiers ([orbdoc](https://orbdoc.com/solutions/medicare-billing-optimization)). |
| **Crushing admin burden** | PCPs spend ~**2 hours on paperwork per 1 hour** of care; EHR inbox, prior auth, and quality reporting are the top burnout drivers ([Commonwealth Fund](https://www.commonwealthfund.org/publications/issue-briefs/2025/oct/administrative-burden-primary-care-causes-potential-solutions), [Tebra](https://www.tebra.com/theintake/staffing-solutions/primary-care-physician-burnout-data)). |
| **Falling real reimbursement** | Medicare physician pay is **down ~29% in real terms since 2001**; 2025 PFS cut rates ~2.93%. Margins are thin ([Medical Economics](https://www.medicaleconomics.com/view/the-primary-care-practice-crisis-it-s-time-to-play-offense)). |
| **Care-management revenue is hard to operationalize** | APCM (2025) removed the time-logging barrier and gives predictable monthly revenue with no downside risk — but small practices struggle with **enrollment, eligibility identification, and workflow** ([PCC](https://thepcc.org/news/advanced-primary-care-management-apcm-is-working-heres-what-practices-need-to-know/), [Prevounce](https://www.prevounce.com/a-comprehensive-guide-to-advanced-primary-care-management)). |
| **Care gaps are found by hand** | Closing gaps (AWVs, screenings, follow-ups) means manually combing records and calling patients — staff don't have time ([ChartSpan](https://www.chartspan.com/blog/what-are-gaps-in-care-and-how-to-close-them/)). |
| **Staffing shortage** | Practices can't hire/retain the care coordinators the vendor model assumes. |

## 2. The competitive gap (where we win)
The care-management software market is **crowded but resented**:
- Full-service vendors **take 40–60% of the Medicare revenue** ([Mindbowser](https://www.mindbowser.com/chronic-care-management-software-pricing/), [ThoroughCare](https://www.thoroughcare.net/blog/care-coordination-software-chronic-care-management-ccm-cost)).
- Software-only platforms charge **$5–25 per patient per month** — a metered cost that scares thin-margin practices.
- Both assume the practice has staff to run the program.

**The unmet need:** *"Help me capture this revenue without (a) surrendering half of it to a vendor, (b) buying heavy software metered per patient, or (c) hiring staff I can't find."*

That is precisely the founder's edge — she's the independent expert who profits from *advice, not rev-share*. The product productizes that.

## 3. The product: "Practice Lens — See the Medicare revenue your practice is missing"
*(Product brand: **Practice Lens**. Company: Campbell3, LLC. Tagline: "See the Medicare revenue your practice is missing.")*
A **flat-fee SaaS** that turns the founder's expertise into a tool a small practice runs itself. Three layers:

**A. Revenue Finder (free — the hook).** The existing engine: five numbers → headline uncaptured revenue +
scenarios. Captures the lead and creates the "I need this" pull. *(Already built.)*

**B. Capture Playbook (the core paid value).** A guided program-in-a-box for APCM, TCM, and AWV:
- Eligibility rules in plain language (who qualifies for each APCM tier; who's AWV-due; post-discharge TCM windows).
- Enrollment scripts, consent templates, monthly service-element checklists.
- Compliance guardrails tied to CMS basis (reuse the Blueprint's compliance registry).
- Billing cheat-sheets (codes, what to document, common denial traps).
- **Kept current** as CMS rules/rates change — that ongoing accuracy is the moat and the reason to keep subscribing.

**C. Capture Dashboard (the sticky tool).** The practice tracks its program and sees revenue captured vs.
the potential the Finder identified — a live "you've captured $X of your $Y opportunity" gauge, monthly
billing worklists, and AWV-due reminders.

**Positioning line:** *"Capture your Medicare care-management revenue and keep 100% of it. No revenue share,
no per-patient fees, no new hires. A flat monthly tool that tells your team exactly what to bill — and walks
them through it."*

## 4. The critical design fork — PHI or not (decide before building)
| | **Option A — No PHI (recommended MVP)** | **Option B — PHI / patient roster** |
|---|---|---|
| What it stores | Counts and program status only; practice keeps patient names in their EHR | Patient roster + per-patient service logs |
| Value | Playbook + count-based dashboard + worklist templates | Auto-tracks each patient, generates exact billing lists |
| Compliance | **No HIPAA BAA needed** — fast, cheap, low liability | Requires HIPAA compliance, BAAs, security audits |
| Build/cost | Light; ship in weeks | Heavy; months + ongoing security cost |
| Stickiness | Moderate | High |

**Recommendation:** launch **Option A** (no PHI). It's the low-friction, no-IT-lift, no-BAA product independent
practices adopt fastest — and it matches the founder's existing "five numbers, no PHI" model. Graduate to
Option B (or an EHR integration) only once there's paying demand and resources for HIPAA infrastructure.

## 5. Pricing (flat fee — the anti-vendor angle)
Practices hate per-patient and rev-share pricing, so **price flat** — that *is* the differentiator. ROI is
enormous (a 300-patient APCM panel is ~$15K/month gross; a vendor would take $6K–9K of it).

| Tier | Price | For |
|---|---|---|
| **Revenue Finder** | **Free** | Lead magnet — anyone, any time |
| **Starter** | **$199/mo** | Solo / 1–2 providers; Playbook + Dashboard, one program (APCM or AWV) |
| **Practice** | **$399/mo** | 3–6 providers; all programs (APCM + TCM + AWV), multi-provider dashboard |
| **Group** | **$899/mo** | Multi-site independent groups (Genesis, Preferred Primary Care, etc.) |

Annual billing ~2 months free. Even at $399/mo, a practice capturing one extra $50/mo APCM patient pays for
the whole tool in a week. Undercut the vendors on price *and* let the practice keep 100%.

## 6. MVP scope (what to build first)
1. **Revenue Finder** as a hosted web app (the phase-two spec already written — `instant-estimate-app-spec.md`).
2. **Capture Playbook** as gated content (the founder's expertise; reuses Blueprint sections + compliance registry).
3. **Capture Dashboard v1** — count-based (Option A): enter enrolled counts + services rendered, see captured
   vs. potential, AWV-due reminders, monthly billing checklist export.
4. **Accounts + flat-fee billing** (Stripe). No EHR integration in MVP.

Built on the existing `engine.py` / rate table / compliance registry — the analytical core is done; this is a
web/app layer plus subscription plumbing.

## 7. Why practices would actually enjoy it
- **It pays for itself in days** and they keep all the revenue.
- **No new staff, no EHR project, no PHI risk** — the #1 reasons practices avoid care-management vendors.
- **It removes guesswork**, not adds clicks — it tells them what to bill and how, which *reduces* admin burden.
- **It's from an independent expert, not a vendor with an angle** — trust is the brand.

## 8. Open decisions for the founder
1. **PHI fork:** confirm Option A (no PHI) for MVP. *(Recommended.)*
2. **Brand:** DECIDED — single brand **Practice Lens** (company: Campbell3, LLC), tagline "See the Medicare
   revenue your practice is missing." Modules use **descriptive names** (no separate trademark needed):
   **Revenue Finder** (free), **Capture Playbook**, **Capture Dashboard**.
   - *Trademark check (informal, 2026-06):* "Practice Lens" — no federal registration found; the only
     "Practice Lens" in use is an **allied-education platform** (different field → low conflict risk for
     healthcare-revenue SaaS), but `practicelens.com` is taken → use an alternate domain
     (`.io`/`.health`/`.app` or `get`/`try` prefix). **"CareCapture" was rejected** — already used by
     multiple healthcare-tech companies (Tulio Health's CareCapture app, Care Capture Inc., CareCapture AI)
     and domains taken; too much likelihood of confusion in-category. Do a formal USPTO/attorney clearance
     on "Practice Lens" before filing.
3. **Scope of v1:** Finder + Playbook first (content-only, fastest to revenue), then add the Dashboard? Or all three at once?
4. **Build path:** this is a real software build (weeks, not the afternoon the Blueprint took). Decide build appetite/budget before starting.
