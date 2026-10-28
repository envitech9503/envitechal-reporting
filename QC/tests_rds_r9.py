"""RDS release R9 (owner 28-10-2026): the formula library on the manual pages (carbonate by APHA 2320 B, one-plate counts,
triplicate EDTA, results to the table), the table's "+" once per click on the WW manual page, the DW manual "+" without a
script error, and a removed results-table row removes every check that writes to it."""
import os

from django.test import SimpleTestCase

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def src(*p):
    return open(os.path.join(ROOT, *p), encoding='utf-8').read()


class RdsR9(SimpleTestCase):
    def test_manual_library(self):
        lib = src('static', 'js', 'rds_formula_lib.js')
        for t in ('function manualDefaults()', 'function toTable(item, side, val)', "MANUAL = typeof window.populateQCTable !== 'function'",
                  "if (card.closest('#rdsLib'))"):
            self.assertIn(t, lib)

    def test_rows_and_checks_removed_together(self):
        qc = src('static', 'js', 'rds_qc.js')
        self.assertIn("closest('.remove-row-btn, button.bg-red-500')", qc)
        self.assertIn("if (tr && snoOf(tr).indexOf('.') > 0) {", qc)

    def test_manual_pages(self):
        self.assertIn("return;   // R9: the table's \"+\" is handled once", src('templates', 'rds_ww_manual.html'))
        self.assertIn("typeof getCalculationBlock === 'function'", src('templates', 'rds_dw_manual.html'))
        for page in ('rds_dw', 'rds_dw_manual', 'rds_ww', 'rds_ww_manual'):
            self.assertIn("rds_qc.js' %}?v=20261028d", src('templates', page + '.html'))
