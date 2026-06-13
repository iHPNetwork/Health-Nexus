"""
MASTER RATE TABLE  —  single source of truth for every dollar figure used in a Blueprint.
-----------------------------------------------------------------------------------------
Nothing in the pipeline is allowed to hard-code a reimbursement rate. Every rate the
engine uses is pulled from this file by name. The self-check gate confirms that no
"orphan" rate (a number not present here) ever reaches a calculation.

FOUNDER — READ THIS BEFORE YOUR FIRST PAID CLIENT
-------------------------------------------------
The dollar values below are national, non-facility 2026 Medicare Physician Fee Schedule
figures, verified 2026-06-12 against multiple independent sources reporting the CY 2026
PFS Final Rule (CMS-1832-F, issued 2025-10-31, effective 2026-01-01). Where sources
differed by pennies (CMS finalized TWO 2026 conversion factors — a slightly higher one
for Qualifying APM Participants), the LOWER non-QP figure was kept so the table stays
conservative.

RECOMMENDED FINAL SPOT-CHECK: before the first paid Blueprint, run the eight codes
through the CMS PFS Look-Up Tool (cms.gov, MAC locality "National Payment Amount",
non-facility) to confirm to-the-penny values for your locality. The verification below
is solid for an opportunity estimate; the lookup tool is the to-the-penny primary source.

Geographic note: PFS amounts vary by locality (GPCI). National averages are used here.
For a real client you may localize, but national-average is defensible and conservative
for a revenue *opportunity* estimate. State this in the methodology (the Blueprint does).
"""

# ----------------------------------------------------------------------------------------
# TABLE STATUS
# ----------------------------------------------------------------------------------------
RATE_TABLE_STATUS = "VERIFIED"           # "PROVISIONAL" | "VERIFIED"
RATE_TABLE_VERIFIED_DATE = "2026-06-12"
RATE_TABLE_BUILD_DATE = "2026-06-12"
RATE_TABLE_SOURCE_NOTE = (
    "2026 Medicare Physician Fee Schedule, national non-facility allowed amounts, per "
    "CY 2026 PFS Final Rule (CMS-1832-F). Cross-verified 2026-06-12 against multiple "
    "independent industry sources (CircleLink, Thoroughcare, ChartSpan, Prevounce, "
    "Rimidi); non-QP conversion-factor figures used where two CFs apply. "
    "APCM = Advanced Primary Care Management (G0556/G0557/G0558, effective 2025)."
)

# Each rate carries: value (USD), unit, source, and a free-text note.
# 'unit' is "per_month" for APCM (a monthly bundle) or "per_service" for visit-based codes.

RATES = {
    # ---- Advanced Primary Care Management (replaces CCM/PCM; monthly bundle, no time log) ----
    "G0556": {  # APCM Level 1 — 1 chronic condition
        "label": "APCM Level 1 (1 chronic condition)",
        "value": 16.37, "unit": "per_month",
        "source": "2026 PFS final rule (verified 2026-06-12)",
        "note": "Lowest tier; patients with a single chronic condition. Was $15.00 provisional.",
    },
    "G0557": {  # APCM Level 2 — 2+ chronic conditions (the workhorse code)
        "label": "APCM Level 2 (2+ chronic conditions)",
        "value": 53.78, "unit": "per_month",
        "source": "2026 PFS final rule (verified 2026-06-12)",
        "note": "Most Medicare patients land here. Primary revenue driver. +10.4% vs 2025 "
                "($48.84). Non-QP CF figure; QP figure is ~$53.91. Was $50.00 provisional.",
    },
    "G0558": {  # APCM Level 3 — 2+ chronic conditions AND QMB (dual-eligible)
        "label": "APCM Level 3 (2+ chronic + QMB / dual-eligible)",
        "value": 117.24, "unit": "per_month",
        "source": "2026 PFS final rule (verified 2026-06-12)",
        "note": "Highest tier; QMB-designated dual-eligible patients. Was $110.00 provisional.",
    },

    # ---- Chronic Care Management (the OLD model practices bill today; used only to value
    #      existing billing that APCM REPLACES, so we never double-count). ----
    "99490": {
        "label": "CCM, first 20 min (legacy model APCM replaces)",
        "value": 66.13, "unit": "per_month",
        "source": "2026 PFS final rule (verified 2026-06-12)",
        "note": "Used ONLY to value a practice's current care-mgmt billing for net-out. "
                "+9.6% vs 2025 ($60.49). Was $62.00 provisional.",
    },

    # ---- Transitional Care Management (visit-based, post-discharge) ----
    "99495": {
        "label": "TCM, moderate complexity (14-day face-to-face)",
        "value": 220.00, "unit": "per_service",
        "source": "2026 PFS final rule (verified 2026-06-12)",
        "note": "Billed once per eligible discharge. +10% vs 2025. Was $207.00 provisional.",
    },
    "99496": {
        "label": "TCM, high complexity (7-day face-to-face)",
        "value": 298.00, "unit": "per_service",
        "source": "2026 PFS final rule (verified 2026-06-12)",
        "note": "Billed once per eligible high-complexity discharge. +10% vs 2025. "
                "Was $277.00 provisional.",
    },

    # ---- Annual Wellness Visit (visit-based, once per 12 months) ----
    "G0438": {
        "label": "AWV, initial visit",
        "value": 174.00, "unit": "per_service",
        "source": "2026 PFS final rule (verified 2026-06-12)",
        "note": "First AWV a patient ever receives. Was $172.00 provisional.",
    },
    "G0439": {
        "label": "AWV, subsequent visit",
        "value": 138.00, "unit": "per_service",
        "source": "2026 PFS final rule (verified 2026-06-12)",
        "note": "Every AWV after the first; the steady-state majority. Confirmed by two "
                "independent 2026 sources; one outlier (~$120) discarded as inconsistent "
                "with the 2025 baseline (~$126-128). Was $131.00 provisional.",
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
