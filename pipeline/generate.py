#!/usr/bin/env python3
"""
PIPELINE ENTRY POINT  —  intake JSON  ->  self-check gate  ->  HTML + PDF Blueprint.
------------------------------------------------------------------------------------
Usage:
    python3 generate.py inputs_westbrook.json            # -> ../samples/<slug>.html + .pdf
    python3 generate.py inputs_westbrook.json --out-dir ../samples
    python3 generate.py --demo                           # builds the Westbrook sample

The gate is ENFORCED: if the self-check fails, NO PDF is written. This is the brief's
"Output a simple pass/fail result before rendering the PDF" requirement, made literal.

Input JSON schema (the five numbers plus labeling):
{
  "practice_name": "Westbrook Family Medicine",
  "prepared_for": "Dr. ____",
  "prepared_by": "Campbell3, LLC",
  "state": "Ohio",
  "physicians": 4,
  "panel_size": 7500,
  "pct_medicare": 28,
  "pct_ffs_of_medicare": 65,
  "current_cm_patients": 60,
  "medicare_discharges_month": 40
}
"""

import sys, os, json, argparse, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import Inputs, run
from selfcheck import run_self_check, print_report
from blueprint import render
from rates import RATE_TABLE_STATUS


WESTBROOK = {
    "practice_name": "Westbrook Family Medicine",
    "prepared_for": "Dr. [Practice Lead]",
    "prepared_by": "Campbell3, LLC",
    "state": "[State]",
    "physicians": 4,
    "panel_size": 7500,
    "pct_medicare": 28,
    "pct_ffs_of_medicare": 65,
    "current_cm_patients": 60,
    "medicare_discharges_month": 40,
}


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def load_inputs(data: dict) -> Inputs:
    return Inputs(
        practice_name=data["practice_name"],
        physicians=int(data["physicians"]),
        panel_size=int(data["panel_size"]),
        pct_medicare=float(data["pct_medicare"]),
        pct_ffs_of_medicare=float(data["pct_ffs_of_medicare"]),
        current_cm_patients=int(data["current_cm_patients"]),
        medicare_discharges_month=int(data["medicare_discharges_month"]),
        prepared_for=data.get("prepared_for", ""),
        prepared_by=data.get("prepared_by", ""),
        state=data.get("state", ""),
    )


def generate(data: dict, out_dir: str) -> dict:
    inp = load_inputs(data)
    results = run(inp)

    # ---- THE GATE ----
    report = run_self_check(results)
    report_text = print_report(report)
    print(report_text)

    if not report["passed"]:
        print("\n*** SELF-CHECK FAILED — PDF NOT RENDERED. Fix the issues above and re-run. ***")
        return {"passed": False, "html": None, "pdf": None}

    if RATE_TABLE_STATUS != "VERIFIED":
        print("\n[NOTE] Rate table is PROVISIONAL. The Blueprint renders so you can review and "
              "practice, but verify rates in rates.py and set status to VERIFIED before sending "
              "to a paying client.")

    os.makedirs(out_dir, exist_ok=True)
    slug = slugify(inp.practice_name)
    html = render(results, report, report_text)
    html_path = os.path.join(out_dir, f"{slug}.html")
    with open(html_path, "w") as fh:
        fh.write(html)
    print(f"\n[OK] HTML written: {html_path}")

    pdf_path = os.path.join(out_dir, f"{slug}.pdf")
    try:
        from weasyprint import HTML
        HTML(string=html, base_url=out_dir).write_pdf(pdf_path)
        size = os.path.getsize(pdf_path)
        print(f"[OK] PDF written:  {pdf_path}  ({size:,} bytes)")
    except Exception as e:
        pdf_path = None
        print(f"[WARN] PDF render skipped ({e}). Open the HTML and Print -> Save as PDF as a fallback.")

    cons = results["scenarios"]["conservative"]["headline_uncaptured"]
    print(f"\nHeadline (conservative): ${cons:,.0f}  |  Guarantee met: {results['guarantee_met']}")
    return {"passed": True, "html": html_path, "pdf": pdf_path, "results": results}


def main():
    ap = argparse.ArgumentParser(description="Generate a Practice Revenue Blueprint.")
    ap.add_argument("inputs", nargs="?", help="Path to intake JSON file")
    ap.add_argument("--demo", action="store_true", help="Build the Westbrook sample Blueprint")
    ap.add_argument("--out-dir", default=os.path.join(os.path.dirname(__file__), "..", "samples"))
    args = ap.parse_args()

    if args.demo or not args.inputs:
        data = WESTBROOK
        print("Building DEMO Blueprint: Westbrook Family Medicine\n")
    else:
        with open(args.inputs) as fh:
            data = json.load(fh)

    out_dir = os.path.abspath(args.out_dir)
    result = generate(data, out_dir)
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
