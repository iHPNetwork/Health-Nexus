"""
MASTER RATE TABLE  —  single source of truth for every dollar figure used in a Blueprint.
-----------------------------------------------------------------------------------------
Nothing in the pipeline is allowed to hard-code a reimbursement rate. Every rate the
engine uses is pulled from this file by name. The self-check gate confirms that no
"orphan" rate (a number not present here) ever reaches a calculation.

FOUNDER — READ THIS BEFORE YOUR FIRST PAID CLIENT
-------------------------------------------------
The dollar values below are national, non-facility 2026 Medicare Physician Fee Schedule
figures as best understood at build time (June 2026). They are intentionally CONSERVATIVE.
Before you deliver a paid Blueprint:

  1. Open your verified 2026 sample Blueprint / the CMS 2026 PFS final rule.
  2. Confirm each value below. Adjust if your verified source differs.
  3. Change RATE_TABLE_STATUS to "VERIFIED" and set RATE_TABLE_VERIFIED_DATE.

The self-check will print the table's status on every run so you always know whether the
numbers in front of a client are confirmed or still provisional. A Blueprint can still be
generated while status is "PROVISIONAL" (so you can practice), but the self-check will
FLAG it loudly and you should not send it to a paying client until status is "VERIFIED".

Geographic note: PFS amounts vary by locality (GPCI). National averages are used here.
For a real client you may localize, but national-average is defensible and conservative
for a revenue *opportunity* estimate. State this in the methodology (the Blueprint does).
"""

# ----------------------------------------------------------------------------------------
# TABLE STATUS  — flip to "VERIFIED" once the founder confirms every value below.
# ----------------------------------------------------------------------------------------
RATE_TABLE_STATUS = "PROVISIONAL"        # "PROVISIONAL" | "VERIFIED"
RATE_TABLE_VERIFIED_DATE = ""            # e.g. "2026-06-12" once verified
RATE_TABLE_BUILD_DATE = "2026-06-12"
RATE_TABLE_SOURCE_NOTE = (
    "2026 Medicare Physician Fee Schedule, national non-facility allowed amounts. "
    "APCM = Advanced Primary Care Management (G0556/G0557/G0558, effective 2025). "
    "Founder to verify against 2026 CMS PFS final rule / verified sample Blueprint."
)

# Each rate carries: value (USD), unit, source, and a free-text note.
# 'unit' is "per_month" for APCM (a monthly bundle) or "per_service" for visit-based codes.

RATES = {
    # ---- Advanced Primary Care Management (replaces CCM/PCM; monthly bundle, no time log) ----
    "G0556": {  # APCM Level 1 — 1 chronic condition
        "label": "APCM Level 1 (1 chronic condition)",
        "value": 15.00, "unit": "per_month",
        "source": "2026 PFS (provisional)",
        "note": "Lowest tier; patients with a single chronic condition.",
    },
    "G0557": {  # APCM Level 2 — 2+ chronic conditions (the workhorse code)
        "label": "APCM Level 2 (2+ chronic conditions)",
        "value": 50.00, "unit": "per_month",
        "source": "2026 PFS (provisional)",
        "note": "Most Medicare patients land here. Primary revenue driver.",
    },
    "G0558": {  # APCM Level 3 — 2+ chronic conditions AND QMB (dual-eligible)
        "label": "APCM Level 3 (2+ chronic + QMB / dual-eligible)",
        "value": 110.00, "unit": "per_month",
        "source": "2026 PFS (provisional)",
        "note": "Highest tier; QMB-designated dual-eligible patients.",
    },

    # ---- Chronic Care Management (the OLD model practices bill today; used only to value
    #      existing billing that APCM REPLACES, so we never double-count). ----
    "99490": {
        "label": "CCM, first 20 min (legacy model APCM replaces)",
        "value": 62.00, "unit": "per_month",
        "source": "2026 PFS (provisional)",
        "note": "Used ONLY to value a practice's current care-mgmt billing for net-out.",
    },

    # ---- Transitional Care Management (visit-based, post-discharge) ----
    "99495": {
        "label": "TCM, moderate complexity (14-day face-to-face)",
        "value": 207.00, "unit": "per_service",
        "source": "2026 PFS (provisional)",
        "note": "Billed once per eligible discharge.",
    },
    "99496": {
        "label": "TCM, high complexity (7-day face-to-face)",
        "value": 277.00, "unit": "per_service",
        "source": "2026 PFS (provisional)",
        "note": "Billed once per eligible high-complexity discharge.",
    },

    # ---- Annual Wellness Visit (visit-based, once per 12 months) ----
    "G0438": {
        "label": "AWV, initial visit",
        "value": 172.00, "unit": "per_service",
        "source": "2026 PFS (provisional)",
        "note": "First AWV a patient ever receives.",
    },
    "G0439": {
        "label": "AWV, subsequent visit",
        "value": 131.00, "unit": "per_service",
        "source": "2026 PFS (provisional)",
        "note": "Every AWV after the first; the steady-state majority.",
    },
}


def rate(code: str) -> float:
    """Return the dollar value for a code, or raise if it is not in the master table.

    The self-check relies on this raising for any unknown code so that no calculation
    can ever use a number that is not registered and (eventually) verified here.
    """
    if code not in RATES:
        raise KeyError(
            f"Rate '{code}' is not in the master rate table. "
            f"Every dollar figure must be registered in rates.py. Refusing to guess."
        )
    return RATES[code]["value"]


def annualize(code: str) -> float:
    """Per_month rates -> annual; per_service rates returned as-is (per service)."""
    r = RATES[code]
    return r["value"] * 12 if r["unit"] == "per_month" else r["value"]


# ----------------------------------------------------------------------------------------
# COST ASSUMPTIONS  — used for the three operational-path net-revenue comparison.
# These are clearly-labeled planning assumptions, not CMS figures. Founder may tune them.
# ----------------------------------------------------------------------------------------
COST_ASSUMPTIONS = {
    "care_coordinator_loaded_annual": 72000.0,   # 1.0 FTE RN/LPN care coordinator, loaded
    "patients_per_coordinator_fte": 450,         # panel one coordinator can manage under APCM
                                                 # (higher than legacy CCM's ~250 because APCM
                                                 #  removed minute-by-minute time logging)
    "software_platform_annual": 6000.0,          # care-mgmt tracking software, in-house
    "inhouse_onboarding_one_time": 4000.0,       # first-year setup/training
    "turnkey_vendor_revenue_share": 0.45,        # vendor keeps 45% of care-mgmt revenue
    "turnkey_practice_oversight_annual": 8000.0, # practice clinical oversight (light)
    "hybrid_vendor_revenue_share": 0.28,         # vendor keeps 28% (outreach labor only)
    "hybrid_practice_fte_fraction": 0.5,         # practice runs 0.5 FTE for clinical/enroll
}


# ----------------------------------------------------------------------------------------
# CLINICAL / ELIGIBILITY ASSUMPTIONS  — the funnel parameters. Conservative by design.
# Founder confirms the starred (*) ones on the 15-minute intake call.
# ----------------------------------------------------------------------------------------
CLINICAL_ASSUMPTIONS = {
    # APCM tier mix among enrolled patients (must sum to 1.0)
    "apcm_mix_level1": 0.15,   # ~1 chronic condition
    "apcm_mix_level2": 0.73,   # 2+ chronic conditions (the majority)
    "apcm_mix_level3": 0.12,   # 2+ chronic + QMB / dual-eligible

    # APCM enrollment rates (% of eligible FFS Medicare panel actually enrolled)
    "apcm_enroll_conservative": 0.25,
    "apcm_enroll_moderate": 0.40,
    "apcm_enroll_optimistic": 0.55,

    # TCM capture (% of eligible Medicare discharges converted to a billed TCM)
    "tcm_capture_conservative": 0.30,
    "tcm_capture_moderate": 0.45,
    "tcm_capture_optimistic": 0.60,
    # TCM complexity mix (must sum to 1.0)
    "tcm_mix_moderate_99495": 0.60,
    "tcm_mix_high_99496": 0.40,

    # AWV — current completion is *assumed* (not one of the five intake numbers) and
    # CONFIRMED on the intake call. Target completion drives the three scenarios.
    "awv_current_completion_assumed": 0.30,   # * confirm on call
    "awv_target_conservative": 0.45,
    "awv_target_moderate": 0.55,
    "awv_target_optimistic": 0.65,
    # AWV initial/subsequent mix (steady state is mostly subsequent)
    "awv_mix_initial_G0438": 0.15,
    "awv_mix_subsequent_G0439": 0.85,
}

# The $50k guarantee threshold (conservative scenario must clear this).
GUARANTEE_THRESHOLD = 50000.0
