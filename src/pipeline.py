from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.sample_data import ensure_invoice_dataset


def classify_invoice(row: pd.Series) -> dict:
    amount_delta = round(float(row["invoice_amount"] - row["po_amount"]), 2)
    requires_human_review = False
    reasons: list[str] = []

    if int(row["has_required_fields"]) == 0:
        requires_human_review = True
        reasons.append("missing_required_fields")
    if int(row["duplicate_invoice"]) == 1:
        requires_human_review = True
        reasons.append("duplicate_invoice")
    if int(row["cost_center_valid"]) == 0:
        requires_human_review = True
        reasons.append("invalid_cost_center")
    if abs(amount_delta) > 20:
        requires_human_review = True
        reasons.append("po_amount_mismatch")
    if float(row["ocr_confidence"]) < 0.8:
        requires_human_review = True
        reasons.append("low_ocr_confidence")

    status = "manual_review" if requires_human_review else "auto_approved"
    if int(row["duplicate_invoice"]) == 1:
        status = "blocked"

    return {
        "invoice_id": row["invoice_id"],
        "supplier_name": row["supplier_name"],
        "status": status,
        "requires_human_review": requires_human_review,
        "amount_delta": amount_delta,
        "reasons": reasons or ["no_exception_detected"],
    }


def run_invoice_processing(base_dir: str | Path) -> dict:
    base_path = Path(base_dir)
    dataset_path = ensure_invoice_dataset(base_path)
    dataframe = pd.read_csv(dataset_path)
    decisions = [classify_invoice(row) for _, row in dataframe.iterrows()]
    decisions_df = pd.DataFrame(decisions)

    output_dir = base_path / "output"
    processed_dir = base_path / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    decisions_path = output_dir / "invoice_decisions.csv"
    report_path = processed_dir / "invoice_processing_report.json"
    decisions_df.to_csv(decisions_path, index=False)

    summary = {
        "runtime_mode": "uipath_style_local_simulation",
        "invoice_count": int(len(dataframe)),
        "auto_approved": int((decisions_df["status"] == "auto_approved").sum()),
        "manual_review_queue": int((decisions_df["status"] == "manual_review").sum()),
        "blocked": int((decisions_df["status"] == "blocked").sum()),
        "average_ocr_confidence": round(float(dataframe["ocr_confidence"].mean()), 4),
        "decision_artifact": str(decisions_path),
        "report_artifact": str(report_path),
        "workflow_artifact": str(base_path / "workflows" / "Main.xaml"),
    }

    report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary
