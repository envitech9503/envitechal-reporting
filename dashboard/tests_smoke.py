"""Characterization / smoke tests for the Envi Tech AL LIMS.

These lock in the CURRENT known-good security behaviour (authentication, CSRF
protection, basic page availability and a query-count ceiling) so that future
refactors cannot silently regress them. They are deliberately conservative and
data-independent, so they pass against a freshly-migrated, empty test database.

Requests use secure=True because the live site enforces SECURE_SSL_REDIRECT; a
plain HTTP test request would be 301-redirected to HTTPS before reaching the view.

Run:
    python manage.py test dashboard.tests_smoke -v2

The test runner builds its own isolated in-memory SQLite test database from
migrations; it never touches the live PostgreSQL data.
"""
from django.contrib.auth import get_user_model
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext


class SmokeSecurityTests(TestCase):
    """Seven guardrail tests covering auth, CSRF and query budget."""

    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.user = cls.User.objects.create_superuser(
            username="smoke_tester",
            email="smoke@example.com",
            password="sMoke-Test-Pass-2026",
        )

    def test_login_page_returns_200(self):
        """The login page is publicly reachable."""
        self.assertEqual(Client().get("/login/", secure=True).status_code, 200)

    def test_anonymous_is_redirected_to_login(self):
        """An anonymous request to a protected page redirects to login."""
        resp = Client().get("/dashboard/equipment/", secure=True)
        self.assertIn(resp.status_code, (301, 302))
        self.assertIn("/login", resp["Location"])

    def test_equipment_loads_for_authenticated_user(self):
        c = Client()
        c.force_login(self.user)
        self.assertEqual(c.get("/dashboard/equipment/", secure=True).status_code, 200)

    def test_chemicals_loads_for_authenticated_user(self):
        c = Client()
        c.force_login(self.user)
        self.assertEqual(c.get("/dashboard/chemicals/", secure=True).status_code, 200)

    def test_csrf_blocks_tokenless_post(self):
        """A POST without a CSRF token is rejected with 403."""
        c = Client(enforce_csrf_checks=True)
        resp = c.post("/login/", {"username": "x", "password": "y"}, secure=True)
        self.assertEqual(resp.status_code, 403)

    def test_login_form_serves_csrf_token(self):
        """CSRF issues a token + cookie for the login form, so legitimate posts can
        carry one (the complement of test_csrf_blocks_tokenless_post)."""
        c = Client()
        page = c.get("/login/", secure=True)
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"csrfmiddlewaretoken", page.content)
        self.assertIn("csrftoken", c.cookies)

    def test_equipment_list_within_query_budget(self):
        """The equipment list stays within a sane query ceiling (N+1 guard)."""
        c = Client()
        c.force_login(self.user)
        with CaptureQueriesContext(connection) as ctx:
            c.get("/dashboard/equipment/", secure=True)
        self.assertLess(
            len(ctx.captured_queries), 50,
            msg="equipment list used %d queries (budget 50)" % len(ctx.captured_queries),
        )


class NavigationSmokeTests(TestCase):
    """Every main navigation page loads (HTTP 200) for an authenticated
    superuser -- a broad guardrail across all apps that catches import errors,
    template breaks and crashes on the primary pages (empty test DB)."""

    NAV_URL_NAMES = [
        "home", "nav", "sample_main", "qc_main",
        "certificate", "job_main", "loggingList", "audit",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username="nav_tester", email="nav@example.com",
            password="Nav-Test-Pass-2026",
        )

    def test_main_nav_pages_load(self):
        from django.urls import reverse
        c = Client()
        c.force_login(self.user)
        for name in self.NAV_URL_NAMES:
            with self.subTest(page=name):
                resp = c.get(reverse(name), secure=True)
                self.assertEqual(resp.status_code, 200)
