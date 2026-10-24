"""Users who left the company are retired, never deleted (24-10-2026).

    manage.py test dashboard.tests_retire_users
"""
import io

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase, override_settings

from EnviTechAlApp.models import Signatures, AuditLog
from EnviTechAlApp.user_retire import retire, linked_counts


@override_settings(OFFICE_EXTRA_IPS=['127.0.0.1'], OFFICE_IP_EXEMPT_USERS=['ImranKazmi'])
class RetireUsersTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        U = get_user_model()
        cls.ceo = U.objects.create_superuser('ImranKazmi', 'c@x.c', 'pw-ceo-123456')
        cls.left = U.objects.create_superuser('Leaver', 'l@x.c', 'pw-lev-123456', first_name='Saba', last_name='Qadeer')
        cls.sig = Signatures.objects.create(user=cls.left, office='Lahore')
        AuditLog.objects.create(user=cls.left, action='made a report', created_by=cls.left)

    def test_retire_keeps_everything(self):
        before = linked_counts(self.left)
        self.assertGreaterEqual(before.get('EnviTechAlApp.AuditLog', 0), 1)
        ch = retire(self.left, by=self.ceo, reason='left the company')
        self.left.refresh_from_db()
        self.assertIn('deactivated', ch)
        self.assertFalse(self.left.is_active or self.left.is_superuser or self.left.is_staff or self.left.has_usable_password())
        self.assertTrue(Signatures.objects.filter(pk=self.sig.pk, user=self.left).exists())       # e-signature row kept
        self.assertEqual(self.left.get_full_name(), 'Saba Qadeer')
        self.assertTrue(AuditLog.objects.filter(action__startswith='Retired user Leaver').exists())
        self.assertEqual(retire(self.left), [])                                                     # idempotent

    def test_retired_cannot_sign_in_and_session_ends(self):
        c = Client(); c.force_login(self.left)
        retire(self.left)
        r = c.get('/qc/control-charts/', secure=True)
        self.assertNotEqual(r.status_code, 200)
        self.assertNotEqual(Client().post('/login/', {'username': 'Leaver', 'password': 'pw-lev-123456'}, secure=True).status_code, 302)

    def test_admin_cannot_delete_and_can_retire(self):
        c = Client(); c.force_login(self.ceo)
        r = c.get('/admin/auth/user/%d/delete/' % self.left.pk, secure=True)
        self.assertIn(r.status_code, (302, 403))
        self.assertTrue(get_user_model().objects.filter(pk=self.left.pk).exists())
        r = c.post('/admin/auth/user/', {'action': 'retire_selected', '_selected_action': [self.left.pk, self.ceo.pk]}, secure=True)
        self.assertEqual(r.status_code, 302)
        self.left.refresh_from_db(); self.ceo.refresh_from_db()
        self.assertFalse(self.left.is_active); self.assertTrue(self.ceo.is_active)                # the CEO is never retired
        r = c.get('/admin/auth/user/', secure=True)
        self.assertEqual(r.status_code, 302); self.assertIn('is_active__exact=1', r['Location'])  # default list = active users
        r = c.get('/admin/auth/user/?is_active__exact=1', secure=True)
        self.assertNotContains(r, '>Leaver<'); self.assertNotContains(r, 'delete_selected')

    def test_command_dry_run_and_apply(self):
        out = io.StringIO(); call_command('retire_users', 'leaver', stdout=out)
        self.assertIn('dry run', out.getvalue()); self.left.refresh_from_db(); self.assertTrue(self.left.is_active)
        out = io.StringIO(); call_command('retire_users', 'Leaver', '--apply', stdout=out)
        self.left.refresh_from_db(); self.assertFalse(self.left.is_active)
        with self.assertRaises(Exception):
            call_command('retire_users', 'ImranKazmi', '--apply', stdout=io.StringIO())
