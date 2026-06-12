"""
CALCULATION ENGINE  —  five intake numbers  ->  three scenarios across APCM, TCM, AWV.
---------------------------------------------------------------------------------------
This module contains NO dollar figures of its own. Every rate comes from rates.py.
It produces a single structured `results` dict that the self-check validates and the
renderer turns into a Blueprint. Keeping calculation and presentation separate is what
lets the self-check independently recompute the math (see selfcheck.py).

THE FIVE INTAKE NUMBERS (from the one-page form / 15-minute call):
  1. panel_size                 active patient panel size                       (int)
  2. pct_medicare               % of panel that is Medicare                     (0-100)
  3. pct_ffs_of_medicare        % of Medicare that is TRADITIONAL fee-for-service(0-100)
                                (Medicare Advantage is excluded — APCM FFS billing
                                 mechanics differ; we stay conservative and count FFS only)
  4. current_cm_patients        patients currently billed monthly care mgmt (CCM/APCM)
  5. medicare_discharges_month  Medicare hospital discharges per month          (int)

Anything not in these five (e.g. current AWV completion, tier mix) comes from the
clearly-labeled assumptions in rates.py and is confirmed on the intake call.
"""

from dataclasses import dataclass, field
from rates import (
    rate, annualize, RATES,
    CLINICAL_ASSUMPTIONS as CA,
    COST_ASSUMPTIONS as CO,
    GUARANTEE_THRESHOLD,
)


@dataclass
class Inputs:
    practice_name: str
    physicians: int
    panel_size: int
    pct_medicare: float
    pct_ffs_of_medicare: float
    current_cm_patients: int
    medicare_discharges_month: int
    prepared_for: str = ""          # contact name on the cover
    prepared_by: str = ""           # firm name
    state: str = ""

    def validate(self):
        errs = []
        if self.panel_size <= 0:
            errs.append("panel_size must be > 0")
        for name, v in [("pct_medicare", self.pct_medicare),
                        ("pct_ffs_of_medicare", self.pct_ffs_of_medicare)]:
            if not (0 <= v <= 100):
                errs.append(f"{name} must be between 0 and 100")
        if self.current_cm_patients < 0:
            errs.append("current_cm_patients must be >= 0")
        if self.medicare_discharges_month < 0:
            errs.append("medicare_discharges_month must be >= 0")
        if self.physicians <= 0:
            errs.append("physicians must be > 0")
        if errs:
            raise ValueError("Invalid inputs: " + "; ".join(errs))
        return self


def _round_int(x: float) -> int:
    return int(round(x))


def compute_funnel(inp: Inputs) -> dict:
    """Translate the five numbers into eligible populations."""
    medicare_patients = inp.panel_size * (inp.pct_medicare / 100.0)
    ffs_medicare = medicare_patients * (inp.pct_ffs_of_medicare / 100.0)
    discharges_year = inp.medicare_discharges_month * 12
    return {
        "medicare_patients": _round_int(medicare_patients),
        "ffs_medicare": _round_int(ffs_medicare),
        "ffs_medicare_exact": ffs_medicare,   # keep exact for downstream math
        "discharges_year": discharges_year,
    }


def _apcm_scenario(eligible_ffs: float, enroll_rate: float) -> dict:
    """APCM revenue for one enrollment scenario. Returns gross annual + breakdown.

    APCM is a MONTHLY bundle that REPLACES CCM. We compute total managed patients at the
    scenario enrollment rate, split them across the three tiers, and annualize.
    """
    enrolled = eligible_ffs * enroll_rate
    n1 = enrolled * CA["apcm_mix_level1"]
    n2 = enrolled * CA["apcm_mix_level2"]
    n3 = enrolled * CA["apcm_mix_level3"]
    rev1 = n1 * annualize("G0556")
    rev2 = n2 * annualize("G0557")
    rev3 = n3 * annualize("G0558")
    return {
        "enrolled": _round_int(enrolled),
        "level1_patients": _round_int(n1),
        "level2_patients": _round_int(n2),
        "level3_patients": _round_int(n3),
        "level1_revenue": rev1,
        "level2_revenue": rev2,
        "level3_revenue": rev3,
        "gross_annual": rev1 + rev2 + rev3,
    }


def _existing_cm_annual(inp: Inputs) -> float:
    """Value the care management a practice ALREADY bills, at the legacy CCM rate.
    This is netted out of APCM so we never count revenue twice (APCM replaces CCM)."""
    return inp.current_cm_patients * annualize("99490")


def _tcm_scenario(discharges_year: int, capture_rate: float) -> dict:
    billed = discharges_year * capture_rate
    n_mod = billed * CA["tcm_mix_moderate_99495"]
    n_high = billed * CA["tcm_mix_high_99496"]
    rev = n_mod * rate("99495") + n_high * rate("99496")
    return {
        "billed": _round_int(billed),
        "moderate_99495": _round_int(n_mod),
        "high_99496": _round_int(n_high),
        "gross_annual": rev,
    }


def _awv_scenario(eligible_ffs: float, target_completion: float) -> dict:
    """New AWVs = (target completion - assumed current completion) * eligible, floored at 0."""
    current = CA["awv_current_completion_assumed"]
    new_fraction = max(0.0, target_completion - current)
    new_awv = eligible_ffs * new_fraction
    n_init = new_awv * CA["awv_mix_initial_G0438"]
    n_subs = new_awv * CA["awv_mix_subsequent_G0439"]
    rev = n_init * rate("G0438") + n_subs * rate("G0439")
    return {
        "new_awv": _round_int(new_awv),
        "initial_G0438": _round_int(n_init),
        "subsequent_G0439": _round_int(n_subs),
        "current_completion": current,
        "target_completion": target_completion,
        "gross_annual": rev,
    }


def _build_scenario(name: str, inp: Inputs, funnel: dict,
                    apcm_enroll: float, tcm_capture: float, awv_target: float) -> dict:
    eligible = funnel["ffs_medicare_exact"]
    existing_cm = _existing_cm_annual(inp)

    apcm = _apcm_scenario(eligible, apcm_enroll)
    tcm = _tcm_scenario(funnel["discharges_year"], tcm_capture)
    awv = _awv_scenario(eligible, awv_target)

    # APCM net of what the practice already bills today (replacement, not additive).
    apcm_net_new = max(0.0, apcm["gross_annual"] - existing_cm)

    # Headline = APCM net-new + TCM new + AWV new. TCM/AWV assumed not billed today unless
    # the practice says otherwise (handled via inputs); we treat them as new opportunity.
    headline = apcm_net_new + tcm["gross_annual"] + awv["gross_annual"]

    return {
        "name": name,
        "apcm_enroll_rate": apcm_enroll,
        "tcm_capture_rate": tcm_capture,
        "awv_target": awv_target,
        "apcm": apcm,
        "tcm": tcm,
        "awv": awv,
        "existing_cm_annual": existing_cm,
        "apcm_net_new": apcm_net_new,
        "headline_uncaptured": headline,
    }


def _operational_paths(conservative: dict) -> list:
    """Net revenue after costs for in-house / turnkey / hybrid, using the CONSERVATIVE
    APCM gross (visit-based TCM & AWV are billed in-house regardless, so the path choice
    is really about who runs the monthly care-management program)."""
    apcm_gross = conservative["apcm"]["gross_annual"]
    enrolled = conservative["apcm"]["enrolled"]

    # In-house: staff to the panel size, plus software + first-year onboarding.
    import math
    ftes = max(1, math.ceil(enrolled / CO["patients_per_coordinator_fte"]))
    inhouse_cost = (ftes * CO["care_coordinator_loaded_annual"]
                    + CO["software_platform_annual"]
                    + CO["inhouse_onboarding_one_time"])
    inhouse_net = apcm_gross - inhouse_cost

    # Turnkey vendor: vendor keeps a revenue share; practice does light oversight.
    turnkey_practice_keep = apcm_gross * (1 - CO["turnkey_vendor_revenue_share"])
    turnkey_net = turnkey_practice_keep - CO["turnkey_practice_oversight_annual"]

    # Hybrid: vendor does outreach labor (smaller share); practice runs partial FTE.
    hybrid_practice_keep = apcm_gross * (1 - CO["hybrid_vendor_revenue_share"])
    hybrid_labor = CO["hybrid_practice_fte_fraction"] * CO["care_coordinator_loaded_annual"]
    hybrid_net = hybrid_practice_keep - hybrid_labor

    return [
        {
            "path": "In-house",
            "summary": f"{ftes} FTE care coordinator(s) + software, run entirely by the practice.",
            "gross": apcm_gross,
            "estimated_cost": inhouse_cost,
            "net_year1": inhouse_net,
            "burden": "Highest management burden; highest net revenue once running.",
        },
        {
            "path": "Turnkey vendor",
            "summary": f"Vendor runs outreach + tracking; keeps {int(CO['turnkey_vendor_revenue_share']*100)}% of care-mgmt revenue.",
            "gross": apcm_gross,
            "estimated_cost": apcm_gross - turnkey_practice_keep + CO["turnkey_practice_oversight_annual"],
            "net_year1": turnkey_net,
            "burden": "Lowest burden; lowest net. Fastest to launch.",
        },
        {
            "path": "Hybrid",
            "summary": f"Practice runs clinical/enrollment ({CO['hybrid_practice_fte_fraction']} FTE); vendor does outreach labor, keeps {int(CO['hybrid_vendor_revenue_share']*100)}%.",
            "gross": apcm_gross,
            "estimated_cost": (apcm_gross - hybrid_practice_keep) + hybrid_labor,
            "net_year1": hybrid_net,
            "burden": "Middle ground; balances burden and net revenue.",
        },
    ]


def run(inp: Inputs) -> dict:
    inp.validate()
    funnel = compute_funnel(inp)

    conservative = _build_scenario(
        "Conservative", inp, funnel,
        CA["apcm_enroll_conservative"], CA["tcm_capture_conservative"], CA["awv_target_conservative"])
    moderate = _build_scenario(
        "Moderate", inp, funnel,
        CA["apcm_enroll_moderate"], CA["tcm_capture_moderate"], CA["awv_target_moderate"])
    optimistic = _build_scenario(
        "Optimistic", inp, funnel,
        CA["apcm_enroll_optimistic"], CA["tcm_capture_optimistic"], CA["awv_target_optimistic"])

    paths = _operational_paths(conservative)

    return {
        "inputs": inp,
        "funnel": funnel,
        "scenarios": {
            "conservative": conservative,
            "moderate": moderate,
            "optimistic": optimistic,
        },
        "operational_paths": paths,
        "guarantee_threshold": GUARANTEE_THRESHOLD,
        "guarantee_met": conservative["headline_uncaptured"] >= GUARANTEE_THRESHOLD,
    }
