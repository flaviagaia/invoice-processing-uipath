from __future__ import annotations

import unittest
from pathlib import Path

from src.pipeline import run_invoice_processing


class InvoiceProcessingUiPathTestCase(unittest.TestCase):
    def test_pipeline_contract(self) -> None:
        project_dir = Path(__file__).resolve().parents[1]
        summary = run_invoice_processing(project_dir)
        self.assertEqual(summary["invoice_count"], 6)
        self.assertEqual(summary["auto_approved"], 1)
        self.assertEqual(summary["manual_review_queue"], 4)
        self.assertEqual(summary["blocked"], 1)


if __name__ == "__main__":
    unittest.main()
