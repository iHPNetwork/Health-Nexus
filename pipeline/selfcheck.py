"""
SELF-CHECK GATE  —  runs BEFORE any PDF is rendered. Returns PASS/FAIL.
-----------------------------------------------------------------------
The brief is strict: if a number cannot be verified, it is removed, not softened.
This module re-derives every headline figure with INDEPENDENT arithmetic (it does not
trust engine.py's results) and compares. Any mismatch, any orphan rate, any double-count,
any blown assumption -> FAIL, and the pipeline refuses to render.

Checks implemented (mirrors the brief's gate):
  1. All arithmetic recomputed independently and reconciled to the engine.
  2. Every rate used is registered in the master rate table (no orphan numbers).
  3. Scenario logic checked for double-counting (APCM REPLACES CCM -> net, not additive).
  4. Tier/complexity/AWV mixes each sum to 1.0 (no leaked or invented patients).
  5. The $50k guarantee threshold is evaluated against the CONSERVATIVE scenario.
  6. Headline = APCM_net_new + TCM + AWV, minus existing billing, never double counted.
  7. Rate-table verification status surfaced (PROVISIONAL vs VERIFIED).
  8. Sanity bounds (no negative revenue, enrolled <= eligible, etc.).

A compliance-statement cross-check is included as a static registry: every compliance
line the Blueprint prints is listed here with its CMS basis, and the renderer is only
allowed to print statements whose key passes this gate.
"""

from rates import (
    RATES, annualize, rate,
    CLINICAL_ASSUMPTIONS as CA,
    RATE_TABLE_STATUS, RATE_TABLE_VERIFIED_DATE,
    GUARANTEE_THRESHOLD,
)

TOL = 0.01  # dollar reconciliation tolerance


class Check:
    def __init__(self, name):
        self.name = name
        self.passed = True
        self.lines = []

    def ok(self, msg):
        self.lines.append(("PASS", msg))

    def fail(self, msg):
        self.passed = False
        self.lines.append(("FAIL", msg))

    def warn(self, msg):
        # warnings do not fail the gate but are surfaced loudly
        self.lines.append(("WARN", msg))


# ---- Compliance statement registry: only statements listed here may be printed. ----
# Each maps a key -> (statement, CMS basis). The Blueprint references these by key.
COMPLIANCE_REGISTRY = {
    "apcm_no_time_log": (
        "APCM (G0556/G0557/G0558) does not require minute-by-minute time logging, unlike "
        "legacy CCM. Billing is based on the patient meeting the chronic-condition criteria "
        "and the practice furnishing the APCM service elements within the calendar month.",
        "CMS CY2025 PFS final rule — APCM code family; CMS APCM FAQ.",
    ),
    "apcm_replaces_ccm": (
        "APCM and CCM cannot be billed for the same patient in the same month. APCM is "
        "billed instead of CCM, not in addition to it.",
        "CMS APCM billing guidance — mutually exclusive with CCM/PCM in a month.",
    ),
    "apcm_consent": (
        "Patient consent must be obtained and documented before billing APCM, and the "
        "patient must be informed of any applicable cost-sharing.",
        "CMS APCM service-element requirements (consent).",
    ),
    "apcm_single_practitioner": (
        "Only one practitioner may bill APCM for a given patient per calendar month.",
        "CMS APCM billing guidance — one biller per patient per month.",
    ),
    "tcm_one_per_30": (
        "TCM (99495/99496) is billed once per patient within 30 days of discharge, with a "
        "face-to-face visit inside the required window (14 days moderate / 7 days high) and "
        "interactive contact within 2 business days of discharge.",
        "CMS TCM billing requirements.",
    ),
    "awv_once_per_year": (
        "The Annual Wellness Visit (G0438 initial / G0439 subsequent) is covered once every "
        "12 months and carries no patient cost-sharing when billed as a stand-alone AWV.",
        "CMS AWV coverage rules.",
    ),
    "qmb_no_balance_bill": (
        "QMB (dual-eligible) patients may not be balance-billed for Medicare cost-sharing; "
        "APCM Level 3 (G0558) recognizes this population.",
        "CMS QMB billing protections.",
    ),
}


def _recompute_scenario(inp, funnel, enroll, capture, awv_target):
    """INDEPENDENT recomputation — deliberately written separately from engine.py."""
    eligible = funnel["ffs_medicare_exact"]

    # APCM, recomputed from raw rate values (not via engine helpers)
    enrolled = eligible * enroll
    g0556_yr = RATES["G0556"]["value"] * 12
    g0557_yr = RATES["G0557"]["value"] * 12
    g0558_yr = RATES["G0558"]["value"] * 12
    apcm_gross = (enrolled * CA["apcm_mix_level1"] * g0556_yr
                  + enrolled * CA["apcm_mix_level2"] * g0557_yr
                  + enrolled * CA["apcm_mix_level3"] * g0558_yr)

    existing = inp.current_cm_patients * RATES["99490"]["value"] * 12
    apcm_net = max(0.0, apcm_gross - existing)

    # TCM
    billed = funnel["discharges_year"] * capture
    tcm = (billed * CA["tcm_mix_moderate_99495"] * RATES["99495"]["value"]
           + billed * CA["tcm_mix_high_99496"] * RATES["99496"]["value"])

    # AWV
    new_frac = max(0.0, awv_target - CA["awv_current_completion_assumed"])
    new_awv = eligible * new_frac
    awv = (new_awv * CA["awv_mix_initial_G0438"] * RATES["G0438"]["value"]
           + new_awv * CA["awv_mix_subsequent_G0439"] * RATES["G0439"]["value"])

    return apcm_gross, apcm_net, tcm, awv, apcm_net + tcm + awv


def run_self_check(results: dict) -> dict:
    checks = []
    inp = results["inputs"]
    funnel = results["funnel"]

    # ---- Check 1: rate table registration / no orphan rates ----
    c = Check("Rate registration & table status")
    used_codes = ["G0556", "G0557", "G0558", "99490", "99495", "99496", "G0438", "G0439"]
    for code in used_codes:
        if code not in RATES:
            c.fail(f"Code {code} used but not registered in rates.py")
        else:
            c.ok(f"{code} registered: {RATES[code]['label']} = ${RATES[code]['value']:.2f} "
                 f"{RATES[code]['unit']}")
    if RATE_TABLE_STATUS == "VERIFIED":
        c.ok(f"Rate table status VERIFIED ({RATE_TABLE_VERIFIED_DATE}).")
    else:
        c.warn("Rate table status is PROVISIONAL. Founder must verify every rate against "
               "the 2026 CMS PFS / verified sample Blueprint before sending to a paid client.")
    checks.append(c)

    # ---- Check 2: assumption mixes sum to 1.0 ----
    c = Check("Assumption mixes sum to 1.0 (no leaked/invented patients)")
    mixes = {
        "APCM tier mix": CA["apcm_mix_level1"] + CA["apcm_mix_level2"] + CA["apcm_mix_level3"],
        "TCM complexity mix": CA["tcm_mix_moderate_99495"] + CA["tcm_mix_high_99496"],
        "AWV initial/subsequent mix": CA["awv_mix_initial_G0438"] + CA["awv_mix_subsequent_G0439"],
    }
    for name, total in mixes.items():
        if abs(total - 1.0) > 1e-9:
            c.fail(f"{name} sums to {total:.4f}, not 1.0")
        else:
            c.ok(f"{name} sums to 1.0")
    checks.append(c)

    # ---- Check 3: independent arithmetic reconciliation per scenario ----
    c = Check("Independent arithmetic reconciliation")
    scen_params = {
        "conservative": (CA["apcm_enroll_conservative"], CA["tcm_capture_conservative"], CA["awv_target_conservative"]),
        "moderate": (CA["apcm_enroll_moderate"], CA["tcm_capture_moderate"], CA["awv_target_moderate"]),
        "optimistic": (CA["apcm_enroll_optimistic"], CA["tcm_capture_optimistic"], CA["awv_target_optimistic"]),
    }
    for key, (en, cap, awvt) in scen_params.items():
        s = results["scenarios"][key]
        rc_apcm_gross, rc_apcm_net, rc_tcm, rc_awv, rc_head = _recompute_scenario(
            inp, funnel, en, cap, awvt)
        pairs = [
            ("APCM gross", s["apcm"]["gross_annual"], rc_apcm_gross),
            ("APCM net-new", s["apcm_net_new"], rc_apcm_net),
            ("TCM", s["tcm"]["gross_annual"], rc_tcm),
            ("AWV", s["awv"]["gross_annual"], rc_awv),
            ("Headline", s["headline_uncaptured"], rc_head),
        ]
        for label, eng_v, rc_v in pairs:
            if abs(eng_v - rc_v) > TOL:
                c.fail(f"[{key}] {label}: engine ${eng_v:,.2f} != recheck ${rc_v:,.2f}")
        c.ok(f"[{key}] all 5 figures reconcile (headline ${rc_head:,.0f})")
    checks.append(c)

    # ---- Check 4: double-counting guard (APCM net = gross - existing, additive forbidden) ----
    c = Check("Double-counting guard (APCM replaces CCM)")
    for key in scen_params:
        s = results["scenarios"][key]
        expected_net = max(0.0, s["apcm"]["gross_annual"] - s["existing_cm_annual"])
        if abs(s["apcm_net_new"] - expected_net) > TOL:
            c.fail(f"[{key}] APCM net-new is not gross minus existing billing")
        # headline must equal net + tcm + awv (NOT gross + existing + ...)
        expected_head = s["apcm_net_new"] + s["tcm"]["gross_annual"] + s["awv"]["gross_annual"]
        if abs(s["headline_uncaptured"] - expected_head) > TOL:
            c.fail(f"[{key}] headline is not APCM_net + TCM + AWV")
        else:
            c.ok(f"[{key}] headline = APCM_net + TCM + AWV; existing ${s['existing_cm_annual']:,.0f} netted out")
    checks.append(c)

    # ---- Check 5: sanity bounds ----
    c = Check("Sanity bounds")
    for key in scen_params:
        s = results["scenarios"][key]
        if s["apcm"]["enrolled"] > funnel["ffs_medicare"] + 1:
            c.fail(f"[{key}] enrolled ({s['apcm']['enrolled']}) exceeds eligible FFS Medicare")
        if s["headline_uncaptured"] < 0:
            c.fail(f"[{key}] negative headline revenue")
        for line in ("apcm", "tcm", "awv"):
            if s[line]["gross_annual"] < 0:
                c.fail(f"[{key}] negative {line} revenue")
    # monotonicity: optimistic >= moderate >= conservative
    h = [results["scenarios"][k]["headline_uncaptured"] for k in ("conservative", "moderate", "optimistic")]
    if not (h[0] <= h[1] <= h[2] + TOL):
        c.fail(f"Scenarios not monotonic: {h}")
    else:
        c.ok(f"Scenarios monotonic: ${h[0]:,.0f} <= ${h[1]:,.0f} <= ${h[2]:,.0f}")
    if c.passed and not any(l[0] == "FAIL" for l in c.lines):
        c.ok("All sanity bounds hold.")
    checks.append(c)

    # ---- Check 6: $50k guarantee threshold on CONSERVATIVE scenario ----
    c = Check("$50k guarantee threshold (conservative scenario)")
    cons = results["scenarios"]["conservative"]["headline_uncaptured"]
    if cons >= GUARANTEE_THRESHOLD:
        c.ok(f"Conservative headline ${cons:,.0f} >= ${GUARANTEE_THRESHOLD:,.0f} threshold. "
             f"Guarantee MET — Blueprint may be delivered for payment.")
    else:
        c.warn(f"Conservative headline ${cons:,.0f} is BELOW the ${GUARANTEE_THRESHOLD:,.0f} "
               f"threshold. Per the guarantee, this practice would NOT be charged. Founder "
               f"should decide whether to deliver at no cost or decline.")
    checks.append(c)

    # ---- Check 7: compliance statements are all registered ----
    c = Check("Compliance statements registered with CMS basis")
    for key, (stmt, basis) in COMPLIANCE_REGISTRY.items():
        if not stmt or not basis:
            c.fail(f"Compliance '{key}' missing statement or CMS basis")
        else:
            c.ok(f"'{key}' has CMS basis: {basis}")
    checks.append(c)

    overall = all(ch.passed for ch in checks)
    return {
        "passed": overall,
        "checks": checks,
        "rate_table_status": RATE_TABLE_STATUS,
        "guarantee_met": results["guarantee_met"],
    }


def print_report(report: dict) -> str:
    """Human-readable pass/fail printout (also embedded in the Blueprint as an attestation)."""
    out = []
    out.append("=" * 78)
    out.append("SELF-CHECK GATE REPORT")
    out.append("=" * 78)
    for ch in report["checks"]:
        status = "PASS" if ch.passed else "FAIL"
        out.append(f"\n[{status}] {ch.name}")
        for level, msg in ch.lines:
            out.append(f"    {level}: {msg}")
    out.append("\n" + "-" * 78)
    out.append(f"RATE TABLE STATUS: {report['rate_table_status']}")
    out.append(f"OVERALL GATE: {'PASS — cleared to render' if report['passed'] else 'FAIL — render blocked'}")
    out.append("=" * 78)
    return "\n".join(out)
