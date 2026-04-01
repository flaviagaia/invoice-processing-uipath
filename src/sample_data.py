from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd


INVOICE_ROWS = [
    {
        "invoice_id": "INV-1001",
        "supplier_name": "Alfa Office Supplies",
        "purchase_order": "PO-9001",
        "invoice_amount": 480.0,
        "po_amount": 480.0,
        "currency": "BRL",
        "due_in_days": 12,
        "ocr_confidence": 0.98,
        "has_required_fields": 1,
        "duplicate_invoice": 0,
        "cost_center_valid": 1,
        "payment_terms_valid": 1,
    },
    {
        "invoice_id": "INV-1002",
        "supplier_name": "Beta Logistics",
        "purchase_order": "PO-9002",
        "invoice_amount": 3210.0,
        "po_amount": 3180.0,
        "currency": "BRL",
        "due_in_days": 5,
        "ocr_confidence": 0.93,
        "has_required_fields": 1,
        "duplicate_invoice": 0,
        "cost_center_valid": 1,
        "payment_terms_valid": 1,
    },
    {
        "invoice_id": "INV-1003",
        "supplier_name": "Gamma Telecom",
        "purchase_order": "PO-9003",
        "invoice_amount": 890.0,
        "po_amount": 890.0,
        "currency": "BRL",
        "due_in_days": 20,
        "ocr_confidence": 0.62,
        "has_required_fields": 1,
        "duplicate_invoice": 0,
        "cost_center_valid": 1,
        "payment_terms_valid": 1,
    },
    {
        "invoice_id": "INV-1004",
        "supplier_name": "Delta Services",
        "purchase_order": "PO-9004",
        "invoice_amount": 1440.0,
        "po_amount": 1440.0,
        "currency": "BRL",
        "due_in_days": 7,
        "ocr_confidence": 0.95,
        "has_required_fields": 0,
        "duplicate_invoice": 0,
        "cost_center_valid": 1,
        "payment_terms_valid": 1,
    },
    {
        "invoice_id": "INV-1005",
        "supplier_name": "Beta Logistics",
        "purchase_order": "PO-9002",
        "invoice_amount": 3180.0,
        "po_amount": 3180.0,
        "currency": "BRL",
        "due_in_days": 6,
        "ocr_confidence": 0.97,
        "has_required_fields": 1,
        "duplicate_invoice": 1,
        "cost_center_valid": 1,
        "payment_terms_valid": 1,
    },
    {
        "invoice_id": "INV-1006",
        "supplier_name": "Omega Consulting",
        "purchase_order": "PO-9006",
        "invoice_amount": 5100.0,
        "po_amount": 5100.0,
        "currency": "BRL",
        "due_in_days": 3,
        "ocr_confidence": 0.96,
        "has_required_fields": 1,
        "duplicate_invoice": 0,
        "cost_center_valid": 0,
        "payment_terms_valid": 1,
    },
]


def ensure_invoice_dataset(base_dir: str | Path) -> str:
    base_path = Path(base_dir)
    raw_dir = base_path / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    dataset_path = raw_dir / "incoming_invoices.csv"
    dataframe = pd.DataFrame(INVOICE_ROWS)

    with NamedTemporaryFile("w", suffix=".csv", delete=False, dir=raw_dir, encoding="utf-8") as tmp_file:
        temp_path = Path(tmp_file.name)
    try:
        dataframe.to_csv(temp_path, index=False)
        temp_path.replace(dataset_path)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    return str(dataset_path)
