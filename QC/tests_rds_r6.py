"""RDS release R6 (owner review 28-10-2026): table names on the right rows when N/A parameters are left out, calculation
sections and library cards in the order of the result table, Enterobacteriaceae by plate count."""
import os

from django.test import SimpleTestCase

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def src(*p):
    return open(os.path.join(ROOT, *p), encoding='utf-8').read()


class RdsR6(SimpleTestCase):
    def test_library_rows(self):
        lib = src('static', 'js', 'rds_formula_lib.js')
        self.assertNotIn("document.querySelector('[name=\"parameter_' + (i + 1) + '\"]')", lib)   # row by place in the full list
        self.assertIn('kept.forEach', lib)
        self.assertIn("enterobacteriaceae/, 'plate']", lib)

    def test_order(self):
        js = src('static', 'js', 'rds_qc.js')
        self.assertIn('function orderSections()', js)
        self.assertIn("try { orderSections(); }", js)
        for page in ('rds_dw', 'rds_dw_manual', 'rds_ww', 'rds_ww_manual'):
            s = src('templates', page + '.html')
            self.assertIn("rds_qc.js' %}?v=20261028a", s)
            self.assertIn("rds_formula_lib.js' %}?v=20261028a", s)
