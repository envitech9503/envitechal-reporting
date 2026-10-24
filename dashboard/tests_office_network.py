"""Office-network protection switch per office (24-10-2026).

    manage.py test dashboard.tests_office_network
"""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings

from EnviTechAlApp import office_ip as oip
from EnviTechAlApp.models import OfficeNetwork, OfficeNetworkLog, Signatures

KHI, LHR, OUT = '110.93.247.168', '124.29.208.36', '39.45.1.2'


@override_settings(OFFICE_IP_EXEMPT_USERS=['ImranKazmi'], OFFICE_ALLOWED_IPS=[KHI, LHR], OFFICE_EXTRA_IPS=[], OFFICE_SWITCH_USERS=['ImranKazmi', 'kadmin'])
class OfficeNetworkSwitchTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        U = get_user_model()
        cls.ceo = U.objects.create_superuser('ImranKazmi', 'c@x.c', 'pw-ceo-123456')
        cls.admin = U.objects.create_superuser('kadmin', 'a@x.c', 'pw-adm-123456')
        cls.khi = U.objects.create_user('khi_chem', 'k@x.c', 'pw-khi-123456')
        cls.lhr = U.objects.create_user('lhr_chem', 'l@x.c', 'pw-lhr-123456')
        cls.none = U.objects.create_user('no_office', 'n@x.c', 'pw-non-123456')
        cls.other_admin = U.objects.create_superuser('otheradmin', 'o@x.c', 'pw-oth-123456')     # superuser, not a switch holder
        Signatures.objects.create(user=cls.admin, office='Karachi')
        Signatures.objects.create(user=cls.khi, office='Karachi')
        Signatures.objects.create(user=cls.lhr, office='lahore ')          # case / spaces as typed in the profile

    def setUp(self):
        oip.invalidate()

    def _set(self, loc, on):
        OfficeNetwork.objects.filter(location=loc).update(enforced=on); oip.invalidate()

    def _get(self, user, ip):
        c = Client(); c.force_login(user)
        return c.get('/office-network/', secure=True, HTTP_X_REAL_IP=ip)

    def _login(self, un, pw, ip):
        return Client().post('/login/', {'username': un, 'password': pw}, secure=True, HTTP_X_REAL_IP=ip).status_code

    def test_seed_karachi_on_lahore_off(self):
        r = {o.location: (o.ip_address, o.enforced) for o in OfficeNetwork.objects.all()}
        self.assertEqual(r, {'Karachi': (KHI, True), 'Lahore': (LHR, False)})
        self.assertTrue(OfficeNetworkLog.objects.filter(location='Lahore', action='off').exists())

    def test_lahore_off_frees_lahore_staff_only(self):
        self._set('Lahore', False); self._set('Karachi', True)
        self.assertEqual(self._login('lhr_chem', 'pw-lhr-123456', OUT), 302)
        self.assertEqual(self._login('khi_chem', 'pw-khi-123456', OUT), 403)
        self.assertEqual(self._login('no_office', 'pw-non-123456', OUT), 403)       # no office: not freed by one office
        self.assertEqual(self._login('khi_chem', 'pw-khi-123456', KHI), 302)
        self.assertEqual(self._login('khi_chem', 'pw-khi-123456', LHR), 302)       # any office network is fine

    def test_turning_on_signs_out_open_sessions(self):
        self._set('Lahore', False)
        c = Client(); c.force_login(self.lhr)
        self.assertNotEqual(c.get('/qc/control-charts/', secure=True, HTTP_X_REAL_IP=OUT).status_code, 403)
        self._set('Lahore', True)
        self.assertEqual(c.get('/qc/control-charts/', secure=True, HTTP_X_REAL_IP=OUT).status_code, 403)

    def test_both_off_frees_everyone_and_ceo_always(self):
        self._set('Lahore', False); self._set('Karachi', False)
        self.assertEqual(self._login('no_office', 'pw-non-123456', OUT), 302)
        self._set('Lahore', True); self._set('Karachi', True)
        self.assertEqual(self._login('ImranKazmi', 'pw-ceo-123456', OUT), 302)
        self.assertEqual(self._login('lhr_chem', 'pw-lhr-123456', OUT), 403)

    def test_wrong_password_outside_still_blocked(self):
        self._set('Lahore', False)
        self.assertEqual(self._login('lhr_chem', 'wrong', OUT), 403)

    def test_page_switch_holders_only(self):
        self.assertEqual(self._get(self.khi, KHI).status_code, 403)
        self.assertEqual(self._get(self.other_admin, KHI).status_code, 403)              # being a superuser is not enough
        c = Client(); c.force_login(self.other_admin)
        c.post('/office-network/', {'location': 'Lahore', 'action': 'on', 'reason': 'not allowed'}, secure=True, HTTP_X_REAL_IP=KHI)
        self.assertFalse(OfficeNetwork.objects.get(location='Lahore').enforced)
        self.assertEqual(self._get(self.ceo, OUT).status_code, 200)
        r = self._get(self.admin, KHI)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Office Network Access'); self.assertContains(r, 'Protection OFF')
        self.assertContains(r, 'Turn ON'); self.assertContains(r, 'lhr_chem')

    def test_switch_needs_reason_and_is_logged(self):
        c = Client(); c.force_login(self.admin)
        c.post('/office-network/', {'location': 'Lahore', 'action': 'on', 'reason': ''}, secure=True, HTTP_X_REAL_IP=KHI)
        self.assertFalse(OfficeNetwork.objects.get(location='Lahore').enforced)
        c.post('/office-network/', {'location': 'Lahore', 'action': 'on', 'reason': 'Internet restored'}, secure=True, HTTP_X_REAL_IP=KHI)
        o = OfficeNetwork.objects.get(location='Lahore')
        self.assertTrue(o.enforced); self.assertEqual(o.updated_by, self.admin)
        lg = OfficeNetworkLog.objects.filter(location='Lahore', action='on').first()
        self.assertEqual((lg.old_value, lg.new_value, lg.reason, lg.from_ip), ('OFF', 'ON', 'Internet restored', KHI))
        # takes effect at once in this process
        self.assertEqual(self._login('lhr_chem', 'pw-lhr-123456', OUT), 403)

    def test_ip_change_validated(self):
        c = Client(); c.force_login(self.admin)
        for bad in ('192.168.1.5', 'abc', KHI):                 # private, invalid, the other office's IP
            c.post('/office-network/', {'location': 'Lahore', 'action': 'ip', 'ip_address': bad, 'reason': 'new line'}, secure=True, HTTP_X_REAL_IP=KHI)
            self.assertEqual(OfficeNetwork.objects.get(location='Lahore').ip_address, LHR)
        c.post('/office-network/', {'location': 'Lahore', 'action': 'ip', 'ip_address': '182.185.10.20', 'reason': 'new Storm Fiber IP'}, secure=True, HTTP_X_REAL_IP=KHI)
        self.assertEqual(OfficeNetwork.objects.get(location='Lahore').ip_address, '182.185.10.20')
        self._set('Lahore', True)
        self.assertEqual(self._login('lhr_chem', 'pw-lhr-123456', '182.185.10.20'), 302)
        self.assertEqual(self._login('lhr_chem', 'pw-lhr-123456', LHR), 403)      # old IP no longer an office

    def test_empty_table_fails_closed(self):
        OfficeNetwork.objects.all().delete(); oip.invalidate()
        self.assertEqual(self._login('lhr_chem', 'pw-lhr-123456', OUT), 403)
        self.assertEqual(self._login('lhr_chem', 'pw-lhr-123456', LHR), 302)

    def test_inactive_holder_refused(self):
        self.admin.is_active = False; self.admin.save()
        self.assertFalse(oip.can_switch(self.admin))
        self.admin.is_active = True; self.admin.save()
        self.assertTrue(oip.can_switch(self.admin))

    def test_menu_entry_switch_holders_only(self):
        c = Client(); c.force_login(self.admin)
        self.assertContains(c.get('/management/', secure=True, HTTP_X_REAL_IP=KHI), '/office-network/')
        for u in (self.khi, self.other_admin):
            c2 = Client(); c2.force_login(u)
            self.assertNotContains(c2.get('/management/', secure=True, HTTP_X_REAL_IP=KHI), '/office-network/')
