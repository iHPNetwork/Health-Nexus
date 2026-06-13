"""
BLUEPRINT RENDERER  —  results dict  ->  print-ready HTML (10-12 pages).
------------------------------------------------------------------------
The same HTML is the on-screen artifact AND the source WeasyPrint turns into the PDF.
All compliance language is pulled from selfcheck.COMPLIANCE_REGISTRY by key, so nothing
prints that the self-check has not blessed.
"""

import datetime
from rates import RATES, RATE_TABLE_STATUS, RATE_TABLE_SOURCE_NOTE, COST_ASSUMPTIONS, CLINICAL_ASSUMPTIONS
from selfcheck import COMPLIANCE_REGISTRY


def usd(x, cents=False):
    return f"${x:,.2f}" if cents else f"${x:,.0f}"


def pct(x):
    return f"{x*100:.0f}%"


def _compliance(key):
    stmt, basis = COMPLIANCE_REGISTRY[key]
    return f'<p class="compliance"><span class="cbadge">CMS</span> {stmt} '\
           f'<span class="cbasis">Basis: {basis}</span></p>'


CSS = """
@page {
  size: letter;
  margin: 0.7in 0.75in 0.8in 0.75in;
  @bottom-center { content: "Practice Revenue Blueprint — Confidential — Page " counter(page) " of " counter(pages); font-size: 8pt; color: #8a8a8a; }
}
* { box-sizing: border-box; }
body { font-family: Georgia, 'Times New Roman', serif; color: #222; font-size: 10pt; line-height: 1.4; margin: 0; }
h1, h2, h3, .label, .kpi-big, .brand, th { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
h1 { font-size: 22pt; color: #143d59; margin: 0 0 6px; }
h2 { font-size: 14.5pt; color: #143d59; border-bottom: 2px solid #143d59; padding-bottom: 3px; margin: 0 0 9px; }
h3 { font-size: 11.5pt; color: #1d5b7a; margin: 11px 0 4px; }
p { margin: 0 0 7px; }
.page-break { page-break-before: always; }
.cover { text-align: left; padding-top: 1.2in; }
.cover .brand { font-size: 11pt; letter-spacing: 2px; text-transform: uppercase; color: #1d5b7a; }
.cover h1 { font-size: 30pt; margin-top: 30px; }
.cover .sub { font-size: 14pt; color: #444; margin-top: 8px; }
.cover .meta { margin-top: 45px; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 10pt; color: #333; }
.cover .meta div { margin-bottom: 4px; }
.rule { height: 4px; background: #143d59; width: 90px; margin: 18px 0; }
/* SAMPLE marking — only rendered when the report is flagged as a sample. */
.watermark { position: fixed; top: 42%; left: 0; right: 0; text-align: center;
  transform: rotate(-32deg); font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 120pt; font-weight: 800; letter-spacing: 14px;
  color: rgba(184, 134, 11, 0.10); z-index: 0; }
.samplebanner { background: #b8860b; color: #fff; font-family: 'Helvetica Neue', Arial, sans-serif;
  font-weight: 700; letter-spacing: 2px; text-transform: uppercase; font-size: 11pt;
  padding: 8px 14px; border-radius: 4px; display: inline-block; margin-bottom: 10px; }
.kpi { background: #f3f7fa; border: 1px solid #d5e3ec; border-left: 6px solid #143d59; padding: 12px 16px; margin: 10px 0; }
.kpi .label { font-size: 9pt; letter-spacing: 1px; text-transform: uppercase; color: #1d5b7a; }
.kpi .kpi-big { font-size: 28pt; color: #143d59; font-weight: 700; line-height: 1.1; }
.kpi .note { font-size: 9pt; color: #555; }
table { width: 100%; border-collapse: collapse; margin: 8px 0 10px; font-size: 9pt; }
th { background: #143d59; color: #fff; text-align: left; padding: 5px 8px; font-size: 8.5pt; }
td { padding: 4px 8px; border-bottom: 1px solid #e0e6ea; }
tr:nth-child(even) td { background: #f7fafc; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
.total-row td { font-weight: 700; background: #eef4f8 !important; border-top: 2px solid #143d59; }
.scenario-cols { display: flex; gap: 10px; margin: 12px 0; }
.scol { flex: 1; border: 1px solid #d5e3ec; border-radius: 5px; padding: 12px; }
.scol.conservative { border-top: 5px solid #2e7d32; }
.scol.moderate { border-top: 5px solid #1d5b7a; }
.scol.optimistic { border-top: 5px solid #b8860b; }
.scol .stitle { font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: 700; font-size: 11pt; }
.scol .samt { font-size: 19pt; font-weight: 700; color: #143d59; margin: 6px 0; }
.scol .sline { font-size: 8.5pt; color: #555; }
.compliance { background: #fbfaf5; border-left: 4px solid #b8860b; padding: 7px 11px; font-size: 9pt; margin: 6px 0; }
.cbadge { background: #b8860b; color: #fff; font-size: 7.5pt; padding: 1px 5px; border-radius: 3px; font-family: Arial; letter-spacing: 1px; vertical-align: middle; }
.cbasis { display: block; font-size: 8pt; color: #777; margin-top: 3px; font-style: italic; }
.callout { background: #f3f7fa; border: 1px solid #d5e3ec; padding: 9px 13px; margin: 9px 0; border-radius: 5px; }
.script { background: #f7f7f4; border: 1px solid #ddd; border-radius: 5px; padding: 9px 11px; margin: 7px 0; font-size: 9pt; }
.script .who { font-family: Arial; font-weight: 700; color: #1d5b7a; font-size: 9pt; }
.roadmap td:first-child { font-weight: 700; color: #143d59; white-space: nowrap; }
.small { font-size: 8.5pt; color: #777; }
.attest { font-family: 'Courier New', monospace; font-size: 8.5pt; background: #f4f4f4; border: 1px solid #ddd; padding: 12px; white-space: pre-wrap; }
.passbadge { background: #2e7d32; color: #fff; padding: 3px 9px; border-radius: 3px; font-family: Arial; font-size: 9pt; }
.provisional { background: #b8860b; color:#fff; padding: 2px 7px; border-radius: 3px; font-family: Arial; font-size: 8pt; }
ul, ol { margin: 4px 0 12px; padding-left: 20px; }
li { margin-bottom: 4px; }
.footnote { font-size: 8pt; color: #888; margin-top: 4px; }
"""


def render(results: dict, selfcheck_report: dict, selfcheck_text: str) -> str:
    inp = results["inputs"]
    f = results["funnel"]
    cons = results["scenarios"]["conservative"]
    mod = results["scenarios"]["moderate"]
    opt = results["scenarios"]["optimistic"]
    paths = results["operational_paths"]
    today = datetime.date.today().strftime("%B %d, %Y")
    firm = inp.prepared_by or "Campbell3, LLC"

    status_badge = ('<span class="passbadge">VERIFIED</span>' if RATE_TABLE_STATUS == "VERIFIED"
                    else '<span class="provisional">RATES PROVISIONAL — VERIFY BEFORE CLIENT DELIVERY</span>')

    # Sample marking — only when the report is flagged as an illustrative sample.
    is_sample = getattr(inp, "sample", False)
    watermark = '<div class="watermark">SAMPLE</div>' if is_sample else ''
    cover_banner = ('<div class="samplebanner">Sample — Illustrative Example (not a real practice)</div>'
                    if is_sample else '')
    sample_note = ('<br><strong>This is an illustrative sample</strong> using fictional inputs for '
                   '"Westbrook Family Medicine." It demonstrates the format and method; it is not a '
                   'real practice or a real client\'s data. Your Blueprint will use your own numbers.'
                   if is_sample else '')

    h = []
    # ---------------- PAGE 1: COVER ----------------
    h.append(f"""
    {watermark}
    <div class="cover">
      {cover_banner}
      <div class="brand">{firm}</div>
      <div class="rule"></div>
      <h1>Practice Revenue Blueprint</h1>
      <div class="sub">Uncaptured Medicare Care-Management Revenue Analysis</div>
      <div class="meta">
        <div><strong>Prepared for:</strong> {inp.practice_name}</div>
        <div><strong>Attention:</strong> {inp.prepared_for or '[Practice contact]'}</div>
        <div><strong>Practice profile:</strong> {inp.physicians} physicians · {inp.panel_size:,}-patient panel · {inp.pct_medicare:.0f}% Medicare{(' · ' + inp.state) if inp.state else ''}</div>
        <div><strong>Date:</strong> {today}</div>
        <div><strong>Prepared by:</strong> {(inp.analyst + ' · ') if getattr(inp, 'analyst', '') else ''}{firm}</div>
        <div style="margin-top:14px;">{status_badge}</div>
      </div>
      <p class="small" style="margin-top:55px;">This report contains no protected health information. All figures are derived from five
      practice-level operating numbers supplied by {inp.practice_name}. Estimates are revenue
      <em>opportunity</em> projections, not guarantees of collection. See methodology and assumptions.{sample_note}</p>
    </div>
    """)

    # ---------------- PAGE 2: EXECUTIVE SUMMARY ----------------
    h.append(f"""
    <div class="page-break"></div>
    <h2>Executive Summary</h2>
    <p>In January 2025, Medicare introduced the Advanced Primary Care Management (APCM) codes
    (G0556, G0557, G0558). They replaced the legacy Chronic Care Management model's
    minute-by-minute time-logging requirement — the single biggest reason most primary care
    practices abandoned care-management billing as unsustainable. Most practices have not yet
    adjusted. That gap is money your practice is currently leaving on the table.</p>

    <p>Based on the five numbers {inp.practice_name} provided, here is the conservative estimate
    of new annual Medicare revenue available across three payment models — Advanced Primary Care
    Management (APCM), Transitional Care Management (TCM), and the Annual Wellness Visit (AWV):</p>

    <div class="kpi">
      <div class="label">Conservative estimate · new annual Medicare care-management revenue</div>
      <div class="kpi-big">{usd(cons['headline_uncaptured'])}</div>
      <div class="note">APCM (net of care management you already bill) + TCM + AWV. The moderate and
      optimistic scenarios — and the full method behind this number — are detailed inside.</div>
    </div>

    <div class="scenario-cols">
      <div class="scol conservative"><div class="stitle">Conservative</div>
        <div class="samt">{usd(cons['headline_uncaptured'])}</div>
        <div class="sline">{pct(cons['apcm_enroll_rate'])} APCM enrollment · {pct(cons['tcm_capture_rate'])} TCM capture · {pct(cons['awv_target'])} AWV completion</div></div>
      <div class="scol moderate"><div class="stitle">Moderate</div>
        <div class="samt">{usd(mod['headline_uncaptured'])}</div>
        <div class="sline">{pct(mod['apcm_enroll_rate'])} APCM enrollment · {pct(mod['tcm_capture_rate'])} TCM capture · {pct(mod['awv_target'])} AWV completion</div></div>
      <div class="scol optimistic"><div class="stitle">Optimistic</div>
        <div class="samt">{usd(opt['headline_uncaptured'])}</div>
        <div class="sline">{pct(opt['apcm_enroll_rate'])} APCM enrollment · {pct(opt['tcm_capture_rate'])} TCM capture · {pct(opt['awv_target'])} AWV completion</div></div>
    </div>

    <h3>What this Blueprint gives you</h3>
    <ol>
      <li><strong>The number</strong> — your uncaptured annual revenue, by model, in three honest scenarios.</li>
      <li><strong>Workflow fit</strong> — which models actually fit your {inp.physicians}-physician staffing, and which to skip.</li>
      <li><strong>Three implementation paths</strong> — in-house, turnkey vendor, and hybrid, each with net revenue <em>after</em> realistic cost.</li>
      <li><strong>A 90-day roadmap</strong>, compliance guardrails, and the exact scripts your front desk and care team will use.</li>
    </ol>

    <div class="callout"><strong>The guarantee.</strong> If this Blueprint's conservative scenario does
    not identify at least {usd(results['guarantee_threshold'])} in new annual revenue, you owe nothing.
    For {inp.practice_name}, the conservative figure is <strong>{usd(cons['headline_uncaptured'])}</strong> —
    {'the guarantee is met.' if results['guarantee_met'] else 'below threshold; you would not be charged.'}</div>
    """)

    # ---------------- PAGE 3: YOUR INPUTS & ELIGIBILITY FUNNEL ----------------
    h.append(f"""
    <div class="page-break"></div>
    <h2>Your Numbers &amp; the Eligibility Funnel</h2>
    <p>Everything in this report traces back to five numbers you supplied. No EHR access, no
    patient data. Here is exactly how those five numbers become an eligible population.</p>

    <table>
      <tr><th>The five inputs</th><th class="num">Value</th></tr>
      <tr><td>Active patient panel</td><td class="num">{inp.panel_size:,}</td></tr>
      <tr><td>Percent Medicare</td><td class="num">{inp.pct_medicare:.0f}%</td></tr>
      <tr><td>Percent of Medicare that is traditional fee-for-service</td><td class="num">{inp.pct_ffs_of_medicare:.0f}%</td></tr>
      <tr><td>Patients currently billed monthly for care management</td><td class="num">{inp.current_cm_patients:,}</td></tr>
      <tr><td>Medicare hospital discharges per month</td><td class="num">{inp.medicare_discharges_month:,}</td></tr>
    </table>

    <h3>From panel to eligible population</h3>
    <table>
      <tr><th>Step</th><th>Calculation</th><th class="num">Patients</th></tr>
      <tr><td>Total panel</td><td>given</td><td class="num">{inp.panel_size:,}</td></tr>
      <tr><td>Medicare patients</td><td>{inp.panel_size:,} × {inp.pct_medicare:.0f}%</td><td class="num">{f['medicare_patients']:,}</td></tr>
      <tr><td>Traditional FFS Medicare (APCM/AWV eligible)</td><td>{f['medicare_patients']:,} × {inp.pct_ffs_of_medicare:.0f}%</td><td class="num">{f['ffs_medicare']:,}</td></tr>
      <tr><td>Medicare discharges / year (TCM eligible)</td><td>{inp.medicare_discharges_month:,} × 12</td><td class="num">{f['discharges_year']:,}</td></tr>
    </table>
    <p class="footnote">We count only traditional fee-for-service Medicare for APCM and AWV. Medicare
    Advantage patients are excluded from these estimates — their care-management economics run through
    plan contracts, not the fee schedule. Excluding them keeps this estimate conservative.</p>

    <h3>Why APCM changes the math for you</h3>
    {_compliance('apcm_no_time_log')}
    <p>Under the old CCM rules, a {inp.physicians}-physician practice had to capture and defend 20 minutes
    of documented staff time per patient per month. The labor cost and audit risk made it a wash. APCM
    removes the stopwatch: you bill on the patient's condition profile and the service elements furnished,
    not on logged minutes. That is what turns this from a break-even chore into net revenue.</p>
    """)

    # ---------------- PAGE 4: METHODOLOGY & RATE TABLE ----------------
    rate_rows = ""
    for code in ["G0556", "G0557", "G0558", "99490", "99495", "99496", "G0438", "G0439"]:
        r = RATES[code]
        unit = "per member / month" if r["unit"] == "per_month" else "per service"
        rate_rows += f'<tr><td>{code}</td><td>{r["label"]}</td><td class="num">{usd(r["value"], cents=True)}</td><td>{unit}</td></tr>'

    h.append(f"""
    <div class="page-break"></div>
    <h2>Methodology &amp; Rate Table</h2>
    <p>This Blueprint uses one master rate table. Every dollar figure in every scenario is built only
    from the rates below — nothing is improvised. {RATE_TABLE_SOURCE_NOTE}</p>
    <table>
      <tr><th>Code</th><th>Service</th><th class="num">2026 rate</th><th>Unit</th></tr>
      {rate_rows}
    </table>
    <p class="footnote">Rates are national, non-facility 2026 Medicare Physician Fee Schedule allowed
    amounts. Actual payment varies by locality (GPCI) and payer mix. Status: {RATE_TABLE_STATUS}.</p>

    <h3>How each scenario is built</h3>
    <ul>
      <li><strong>APCM</strong> — eligible FFS Medicare patients × enrollment rate, split across the three
      APCM tiers ({pct(CLINICAL_ASSUMPTIONS['apcm_mix_level1'])} Level 1 / {pct(CLINICAL_ASSUMPTIONS['apcm_mix_level2'])} Level 2 / {pct(CLINICAL_ASSUMPTIONS['apcm_mix_level3'])} Level 3), annualized,
      then <em>reduced</em> by the care management you already bill so nothing is counted twice.</li>
      <li><strong>TCM</strong> — annual Medicare discharges × capture rate, split {pct(CLINICAL_ASSUMPTIONS['tcm_mix_moderate_99495'])}/{pct(CLINICAL_ASSUMPTIONS['tcm_mix_high_99496'])} moderate/high complexity.</li>
      <li><strong>AWV</strong> — eligible FFS Medicare × the gain from assumed current completion
      ({pct(CLINICAL_ASSUMPTIONS['awv_current_completion_assumed'])}, confirmed on your intake call) up to the scenario target.</li>
    </ul>
    <p>The three scenarios differ only in adoption assumptions — enrollment, capture, and completion
    rates. They use identical rates and identical eligibility. Conservative is deliberately low so the
    number you build a decision on is one you can beat, not one you have to hit.</p>
    """)

    # ---------------- PAGE 5: APCM DEEP DIVE (single comparison table) ----------------
    a_c, a_m, a_o = cons["apcm"], mod["apcm"], opt["apcm"]
    h.append(f"""
    <div class="page-break"></div>
    <h2>Advanced Primary Care Management (APCM)</h2>
    <p>APCM is the largest opportunity for {inp.practice_name}, and the one the 2025 rule change
    unlocked. Your eligible pool is <strong>{f['ffs_medicare']:,} traditional FFS Medicare patients</strong>.
    The table compares all three scenarios; tiers are split
    {pct(CLINICAL_ASSUMPTIONS['apcm_mix_level1'])}/{pct(CLINICAL_ASSUMPTIONS['apcm_mix_level2'])}/{pct(CLINICAL_ASSUMPTIONS['apcm_mix_level3'])}
    across Levels 1/2/3.</p>

    <table>
      <tr><th>APCM line</th><th class="num">Conservative</th><th class="num">Moderate</th><th class="num">Optimistic</th></tr>
      <tr><td>Enrollment rate (of eligible)</td><td class="num">{pct(cons['apcm_enroll_rate'])}</td><td class="num">{pct(mod['apcm_enroll_rate'])}</td><td class="num">{pct(opt['apcm_enroll_rate'])}</td></tr>
      <tr><td>Patients enrolled</td><td class="num">{a_c['enrolled']:,}</td><td class="num">{a_m['enrolled']:,}</td><td class="num">{a_o['enrolled']:,}</td></tr>
      <tr><td>Level 1 revenue (G0556, {usd(RATES['G0556']['value']*12)}/yr)</td><td class="num">{usd(a_c['level1_revenue'])}</td><td class="num">{usd(a_m['level1_revenue'])}</td><td class="num">{usd(a_o['level1_revenue'])}</td></tr>
      <tr><td>Level 2 revenue (G0557, {usd(RATES['G0557']['value']*12)}/yr)</td><td class="num">{usd(a_c['level2_revenue'])}</td><td class="num">{usd(a_m['level2_revenue'])}</td><td class="num">{usd(a_o['level2_revenue'])}</td></tr>
      <tr><td>Level 3 revenue (G0558, {usd(RATES['G0558']['value']*12)}/yr)</td><td class="num">{usd(a_c['level3_revenue'])}</td><td class="num">{usd(a_m['level3_revenue'])}</td><td class="num">{usd(a_o['level3_revenue'])}</td></tr>
      <tr class="total-row"><td>APCM gross annual</td><td class="num">{usd(a_c['gross_annual'])}</td><td class="num">{usd(a_m['gross_annual'])}</td><td class="num">{usd(a_o['gross_annual'])}</td></tr>
      <tr><td>Less: care mgmt you already bill</td><td class="num">({usd(cons['existing_cm_annual'])})</td><td class="num">({usd(mod['existing_cm_annual'])})</td><td class="num">({usd(opt['existing_cm_annual'])})</td></tr>
      <tr class="total-row"><td>Net new APCM revenue</td><td class="num">{usd(cons['apcm_net_new'])}</td><td class="num">{usd(mod['apcm_net_new'])}</td><td class="num">{usd(opt['apcm_net_new'])}</td></tr>
    </table>
    <p class="footnote">Level 2 (2+ chronic conditions, {usd(RATES['G0557']['value'])}/member/month) is the
    workhorse — most of your Medicare panel qualifies. Your existing care-management billing
    ({inp.current_cm_patients} patients) is subtracted so nothing is counted twice.</p>

    {_compliance('apcm_replaces_ccm')}
    {_compliance('apcm_single_practitioner')}
    {_compliance('apcm_consent')}
    {_compliance('qmb_no_balance_bill')}
    """)

    # ---------------- PAGE 6: TCM (single comparison table) ----------------
    t_c, t_m, t_o = cons["tcm"], mod["tcm"], opt["tcm"]
    h.append(f"""
    <div class="page-break"></div>
    <h2>Transitional Care Management (TCM)</h2>
    <p>You reported {inp.medicare_discharges_month:,} Medicare discharges per month
    ({f['discharges_year']:,} per year). Each is a billable TCM encounter if your team reaches the
    patient within two business days and sees them inside the required window. Most practices capture
    a fraction today; the scenarios below model closing that gap (mix:
    {pct(CLINICAL_ASSUMPTIONS['tcm_mix_moderate_99495'])} moderate / {pct(CLINICAL_ASSUMPTIONS['tcm_mix_high_99496'])} high complexity).</p>

    <table>
      <tr><th>TCM line</th><th class="num">Conservative</th><th class="num">Moderate</th><th class="num">Optimistic</th></tr>
      <tr><td>Discharge capture rate</td><td class="num">{pct(cons['tcm_capture_rate'])}</td><td class="num">{pct(mod['tcm_capture_rate'])}</td><td class="num">{pct(opt['tcm_capture_rate'])}</td></tr>
      <tr><td>99495 moderate ({usd(RATES['99495']['value'])}) — encounters</td><td class="num">{t_c['moderate_99495']:,}</td><td class="num">{t_m['moderate_99495']:,}</td><td class="num">{t_o['moderate_99495']:,}</td></tr>
      <tr><td>99496 high ({usd(RATES['99496']['value'])}) — encounters</td><td class="num">{t_c['high_99496']:,}</td><td class="num">{t_m['high_99496']:,}</td><td class="num">{t_o['high_99496']:,}</td></tr>
      <tr><td>Total TCM encounters / yr</td><td class="num">{t_c['billed']:,}</td><td class="num">{t_m['billed']:,}</td><td class="num">{t_o['billed']:,}</td></tr>
      <tr class="total-row"><td>TCM annual revenue</td><td class="num">{usd(t_c['gross_annual'])}</td><td class="num">{usd(t_m['gross_annual'])}</td><td class="num">{usd(t_o['gross_annual'])}</td></tr>
    </table>

    {_compliance('tcm_one_per_30')}
    <div class="callout"><strong>Workflow fit note.</strong> TCM revenue depends entirely on a discharge
    alert reaching your team within two business days. If you do not have a reliable discharge feed
    (ADT, hospital fax, or a daily call), start TCM <em>after</em> you have closed that loop — otherwise
    you will bill a handful and miss the window on the rest. This is flagged again in your roadmap.</div>
    """)

    # ---------------- PAGE 7: AWV (single comparison table) ----------------
    w_c, w_m, w_o = cons["awv"], mod["awv"], opt["awv"]
    h.append(f"""
    <div class="page-break"></div>
    <h2>Annual Wellness Visit (AWV)</h2>
    <p>The AWV is the most underused code in primary care. We assume {inp.practice_name} currently
    completes about {pct(CLINICAL_ASSUMPTIONS['awv_current_completion_assumed'])} of eligible AWVs
    (confirm this on your call — it moves the number). Each scenario models lifting completion toward a
    target across your {f['ffs_medicare']:,} eligible patients.</p>

    <table>
      <tr><th>AWV line</th><th class="num">Conservative</th><th class="num">Moderate</th><th class="num">Optimistic</th></tr>
      <tr><td>Completion target</td><td class="num">{pct(cons['awv_target'])}</td><td class="num">{pct(mod['awv_target'])}</td><td class="num">{pct(opt['awv_target'])}</td></tr>
      <tr><td>New AWVs vs. current ({pct(CLINICAL_ASSUMPTIONS['awv_current_completion_assumed'])})</td><td class="num">{w_c['new_awv']:,}</td><td class="num">{w_m['new_awv']:,}</td><td class="num">{w_o['new_awv']:,}</td></tr>
      <tr><td>G0438 initial ({usd(RATES['G0438']['value'])})</td><td class="num">{w_c['initial_G0438']:,}</td><td class="num">{w_m['initial_G0438']:,}</td><td class="num">{w_o['initial_G0438']:,}</td></tr>
      <tr><td>G0439 subsequent ({usd(RATES['G0439']['value'])})</td><td class="num">{w_c['subsequent_G0439']:,}</td><td class="num">{w_m['subsequent_G0439']:,}</td><td class="num">{w_o['subsequent_G0439']:,}</td></tr>
      <tr class="total-row"><td>AWV annual revenue</td><td class="num">{usd(w_c['gross_annual'])}</td><td class="num">{usd(w_m['gross_annual'])}</td><td class="num">{usd(w_o['gross_annual'])}</td></tr>
    </table>

    {_compliance('awv_once_per_year')}
    <p>AWVs also create the documented chronic-condition list that qualifies patients for APCM tiers —
    so AWV and APCM reinforce each other. Practices that run AWVs well find APCM enrollment easier.</p>
    """)

    # ---------------- PAGE 8: THREE OPERATIONAL PATHS ----------------
    path_rows = ""
    for p in paths:
        path_rows += f"""<tr>
          <td><strong>{p['path']}</strong><br><span class="small">{p['summary']}</span></td>
          <td class="num">{usd(p['gross'])}</td>
          <td class="num">{usd(p['estimated_cost'])}</td>
          <td class="num">{usd(p['net_year1'])}</td>
        </tr>"""

    h.append(f"""
    <div class="page-break"></div>
    <h2>Three Implementation Paths — Net Revenue After Cost</h2>
    <p>The number on page two is gross opportunity. What you keep depends on who does the work. Below
    are three honest paths for the APCM program (TCM and AWV are visit-based and billed in-house under
    every path). Figures use the <strong>conservative</strong> APCM scenario, so they are a floor.</p>

    <table>
      <tr><th>Path</th><th class="num">APCM gross (conservative)</th><th class="num">Est. annual cost</th><th class="num">Net year 1</th></tr>
      {path_rows}
    </table>
    <p class="footnote">Cost assumptions: care coordinator loaded at {usd(COST_ASSUMPTIONS['care_coordinator_loaded_annual'])}/yr,
    ~{COST_ASSUMPTIONS['patients_per_coordinator_fte']} patients per FTE; software {usd(COST_ASSUMPTIONS['software_platform_annual'])}/yr;
    turnkey vendor share {pct(COST_ASSUMPTIONS['turnkey_vendor_revenue_share'])}; hybrid vendor share {pct(COST_ASSUMPTIONS['hybrid_vendor_revenue_share'])}.
    These are planning assumptions you can tune; they are not CMS figures.</p>

    <h3>How to choose</h3>
    <ul>
      <li><strong>In-house</strong> keeps the most revenue and builds a durable capability, but you own
      hiring, training, and retention. Best if you have, or will hire, a care coordinator and want the asset.</li>
      <li><strong>Turnkey vendor</strong> launches fastest with the least staff disruption, at the cost of
      the largest revenue share. Best if you want the revenue without adding headcount or process.</li>
      <li><strong>Hybrid</strong> keeps clinical judgment and enrollment in-house while outsourcing the
      outreach labor that eats time. Usually the best risk-adjusted choice for a {inp.physicians}-physician practice.</li>
    </ul>
    <p>No vendor recommendation is embedded in this report, and the firm preparing it does not resell or
    take referral fees from any care-management vendor. The path you pick is yours.</p>
    """)

    # ---------------- PAGE 9: 90-DAY ROADMAP ----------------
    h.append(f"""
    <div class="page-break"></div>
    <h2>90-Day Implementation Roadmap</h2>
    <table class="roadmap">
      <tr><th>Window</th><th>Milestone</th><th>Owner</th></tr>
      <tr><td>Days 1–15</td><td>Pick a path (in-house / turnkey / hybrid). Confirm current AWV completion and discharge-feed reliability. Designate one APCM billing practitioner.</td><td>Physician lead</td></tr>
      <tr><td>Days 1–15</td><td>Pull the list of FFS Medicare patients with 2+ chronic conditions (your APCM Level 2 core). Target list of {cons['apcm']['enrolled']:,}+ for the conservative ramp.</td><td>Office manager</td></tr>
      <tr><td>Days 16–30</td><td>Build consent workflow and the monthly APCM service-element checklist. Train front desk on the enrollment script (next page).</td><td>Care coordinator</td></tr>
      <tr><td>Days 16–45</td><td>Stand up the discharge loop for TCM: ADT feed or daily hospital census call, 2-business-day outreach protocol.</td><td>Care coordinator</td></tr>
      <tr><td>Days 30–60</td><td>Begin APCM enrollment at the practice's pace; bill first month for enrolled cohort. Begin booking AWVs into open slots and pairing them with enrollment.</td><td>Whole team</td></tr>
      <tr><td>Days 60–90</td><td>First full billing month reconciled. Review captured vs. modeled. Adjust enrollment outreach. Decide on staffing for the next ramp tier.</td><td>Physician lead</td></tr>
    </table>
    <div class="callout"><strong>Sequencing matters.</strong> Start with APCM Level 2 enrollment and AWV —
    they are the largest, most predictable dollars and require no external feed. Add TCM only once the
    discharge loop is reliable. Do not try to launch all three in week one.</div>
    """)

    # ---------------- PAGE 10: COMPLIANCE GUARDRAILS ----------------
    all_compliance = "".join(_compliance(k) for k in [
        "apcm_no_time_log", "apcm_replaces_ccm", "apcm_single_practitioner",
        "apcm_consent", "qmb_no_balance_bill", "tcm_one_per_30", "awv_once_per_year"])
    h.append(f"""
    <div class="page-break"></div>
    <h2>Compliance Guardrails</h2>
    <p>Every statement below is tied to a CMS basis and was cross-checked in this report's automated
    self-check before delivery. These are the rules that keep the revenue clean.</p>
    {all_compliance}
    <p class="footnote">This is operational guidance, not legal advice. Confirm current-year specifics
    with your billing compliance resource before go-live. CMS guidance is updated periodically.</p>
    """)

    # ---------------- PAGE 11: SCRIPTS ----------------
    h.append(f"""
    <div class="page-break"></div>
    <h2>Scripts Your Staff Will Use</h2>

    <h3>Front-desk APCM enrollment (at check-in or by phone)</h3>
    <div class="script"><span class="who">Front desk →</span> "Mr./Ms. [name], because you have ongoing
    conditions we help manage, Medicare now covers a monthly care-management service through our office —
    a dedicated person who keeps an eye on your care between visits, coordinates your medications, and is
    your direct line if something changes. Most patients owe little or nothing. Dr. [name] recommends it
    for you. May I have your okay to enroll you today?"</div>

    <h3>Care coordinator monthly touch (APCM)</h3>
    <div class="script"><span class="who">Care coordinator →</span> "Hi [name], this is [coordinator] from
    Dr. [name]'s office — your care-management check-in. How are you doing with [condition]? Any new
    medicines, ER visits, or hospital stays since we talked? Let's make sure your refills and upcoming
    appointments are set." <em>(Document the service elements furnished — no stopwatch required.)</em></div>

    <h3>Post-discharge TCM outreach (within 2 business days)</h3>
    <div class="script"><span class="who">Care coordinator →</span> "Hi [name], I saw you were just in the
    hospital — I'm calling from Dr. [name]'s office to make sure your recovery goes smoothly. Do you have
    all your new medications? Any new symptoms? I'd like to get you in to see Dr. [name] within the next
    [7/14] days — does [day] work?" <em>(Interactive contact within 2 business days is required to bill.)</em></div>

    <h3>AWV invitation</h3>
    <div class="script"><span class="who">Scheduler →</span> "Mr./Ms. [name], you're due for your yearly
    Medicare Wellness Visit — it's fully covered, no cost to you, and it's how we update your care plan and
    catch things early. I have [day/time] open. Shall I book it?"</div>
    """)

    # ---------------- PAGE 12: GUARANTEE, NEXT STEPS, ATTESTATION ----------------
    h.append(f"""
    <div class="page-break"></div>
    <h2>Guarantee, Next Steps &amp; Self-Check Attestation</h2>

    <div class="callout"><strong>The guarantee.</strong> If the conservative scenario in this Blueprint does
    not identify at least {usd(results['guarantee_threshold'])} in new annual revenue, you owe nothing.
    {inp.practice_name}'s conservative figure is <strong>{usd(cons['headline_uncaptured'])}</strong>.</div>

    <h3>Next steps</h3>
    <ol>
      <li><strong>30-minute working session</strong> to walk these numbers and choose a path.</li>
      <li>We finalize your path decision and the first-cohort target list.</li>
      <li>You execute the 90-day roadmap; we are available for the first billing-month reconciliation.</li>
    </ol>

    <h3>Self-check attestation</h3>
    <p>This Blueprint was not delivered until an automated gate independently recomputed every figure,
    verified every rate against the master table, confirmed APCM was netted against existing billing (no
    double-counting), and cross-checked every compliance statement against its CMS basis. The gate result:</p>
    <p><span class="passbadge">SELF-CHECK: {'PASS' if selfcheck_report['passed'] else 'FAIL'}</span>
    &nbsp; Rate table status: <strong>{RATE_TABLE_STATUS}</strong></p>
    <div class="attest">{_compact_attestation(selfcheck_report)}</div>

    <p class="footnote" style="margin-top:20px;">Prepared by {firm}. This analysis estimates revenue
    opportunity based on practice-supplied operating numbers and stated assumptions; it is not a guarantee
    of payment or collection and is not legal or billing-compliance advice. No PHI was used in its preparation.</p>
    """)

    body = "\n".join(h)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Practice Revenue Blueprint — {inp.practice_name}</title>
<style>{CSS}</style></head><body>{body}</body></html>"""


def _escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _compact_attestation(report: dict) -> str:
    """One line per gate check (name + PASS/FAIL) — the full verbose log stays in the
    console output of generate.py; the PDF carries this auditable summary."""
    lines = []
    for ch in report["checks"]:
        status = "PASS" if ch.passed else "FAIL"
        lines.append(f"[{status}]  {ch.name}")
    lines.append("")
    lines.append(f"RATE TABLE: {report['rate_table_status']}")
    lines.append(f"OVERALL GATE: {'PASS — cleared to render' if report['passed'] else 'FAIL — blocked'}")
    return _escape("\n".join(lines))
