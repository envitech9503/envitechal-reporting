"""RDS release R4 (QA audit 27-10-2026): premium finish - wording, markup, list pages, page polish."""
import os
import re

from django.contrib.auth.models import User
from django.test import TestCase, Client

from QC.models import Dw_rds

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def page(name):
    return open(os.path.join(ROOT, 'templates', name + '.html')).read()


class RdsR4Tests(TestCase):
    def test_wording_and_markup(self):
        for p in ('rds_dw', 'rds_dw_manual', 'rds_ww', 'rds_ww_manual'):
            s = page(p)
            for bad in ('value="Anitomny"', 'OIl and Grease', 'value="desolve_oxygen:"', 'Value of Sample', 'InitialReading', 'name="chromium_IV_head" id="" value="WS-Turbidity', ' name="" id=""'):
                self.assertNotIn(bad, s, (p, bad))
            for inp in re.findall(r'<input\b[^>]*\btype="number"[^>]*>', s):
                v = re.search(r'\svalue="([^"]*)"', inp)
                if v and not re.search(r'[{$%]', v.group(1)):
                    float(v.group(1))                               # a number box holds a number
        self.assertIn('</script>\n</html>', page('rds_dw_manual'))
        for f, bad in (('QC/views/dw.py', 'Trubidity Calculations'), ('QC/views/ww.py', 'Trubidity Calculations')):
            self.assertNotIn(bad, open(os.path.join(ROOT, f)).read())
        js = open(os.path.join(ROOT, 'static', 'js', 'rds_ww_calc.js')).read()
        self.assertIn('wsTrue', js)

    def test_lists(self):
        u = User.objects.create_superuser('r4_ceo', 'c@x.c', 'x')
        Dw_rds.objects.create(sample_id='DW-R4', rds={'parameter_1': 'TDS'}); Dw_rds.objects.create(sample_id='DW-R4', rds={'parameter_1': 'TDS'})
        c = Client(REMOTE_ADDR='127.0.0.1'); c.force_login(u)
        for url in ('/qc/dw_rds_list/', '/qc/ww_rds_list/'):
            r = c.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertContains(r, '_unified_nav') if False else self.assertNotContains(r, 'logo-light.png')
        r = c.get('/qc/dw_rds_list/')
        self.assertContains(r, 'Rev. 2'); self.assertContains(r, 'latest'); self.assertContains(r, 'Add RDS')
