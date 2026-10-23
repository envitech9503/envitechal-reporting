"""Seed the document-control revision history (23-10-2026).

Every document-control row in use (InventoryDocControl: chemicals, equipment, reagent preparation, control charts,
per-chart forms, Internal Audit, MOU) becomes revision 1 effective from 01-01-2000, i.e. the revision of every
document issued so far. The numbers that were typed into the PDF code (job completion, logging sheet issue date,
QC raw-data sheets and testing-result printouts) are seeded with exactly the text printed today, so nothing printed
changes on deployment; later revisions are issued on the Document Control register with an effective date.
"""
import datetime

from django.db import migrations

BASELINE = datetime.date(2000, 1, 1)
NOTE = 'Revision in force before revision history (seeded 23-10-2026)'
HARD_CODED = [
    # module, location, doc_no, issue_date, issue_no, rev_no  (as printed by the PDF code on 23-10-2026)
    ('job_completion', 'Karachi', 'ETAL-LAB-704-FF-08', '15-05-2026', '01', '00'),
    ('job_completion', 'Lahore', 'ETAL-LAB-704-FF-08', '15-05-2026', '01', '00'),
    ('logging_sheet', 'Karachi', 'ETAL-LAB-704-FF-1(A)', '17-12-2021', '01', '00'),
    ('logging_sheet', 'Lahore', 'ETAL-LAB-704-FF-1(A)', '05-01-2023', '01', '00'),
    ('qc_rds', '*', 'ETAL-LAB-704-FF-05', '22-12-2025', '02', '01'),
    ('qc_test_results', 'Karachi', 'ETAL-LAB-704-FF-07', '01-08-2022', '01', '00'),
    ('qc_test_results', 'Lahore', 'ETAL-LAB-704-FF-07', '05-01-2023', '01', '00'),
    ('qc_test_results', '*', 'ETAL-LAB-704-FF-05', '22-12-2025', '02', '01'),
]


def seed(apps, schema_editor):
    Mirror = apps.get_model('EnviTechAlApp', 'InventoryDocControl')
    Rev = apps.get_model('EnviTechAlApp', 'DocControlRevision')
    for m in Mirror.objects.all():
        if not ((m.doc_no or '').strip() or (m.issue_date or '').strip()):
            continue
        loc = '*' if m.module.startswith('cc_chart_') else m.location     # a chart's own form belongs to the chart
        if Rev.objects.filter(module=m.module, location=loc).exists():
            continue
        Rev.objects.create(module=m.module, location=loc, doc_no=(m.doc_no or '').strip(), issue_date=(m.issue_date or '').strip(),
                           issue_no=(m.issue_no or '01').strip(), rev_no=(m.rev_no or '00').strip(), effective_from=BASELINE, note=NOTE,
                           created_by_id=m.updated_by_id)
    for module, loc, doc_no, issue_date, issue_no, rev_no in HARD_CODED:
        if not Rev.objects.filter(module=module, location=loc).exists():
            Rev.objects.create(module=module, location=loc, doc_no=doc_no, issue_date=issue_date, issue_no=issue_no, rev_no=rev_no,
                               effective_from=BASELINE, note=NOTE + ' - from the PDF code')
        m, _ = Mirror.objects.get_or_create(module=module, location=loc)
        if not (m.doc_no or m.issue_date):
            m.doc_no, m.issue_date, m.issue_no, m.rev_no = doc_no, issue_date, issue_no, rev_no
            m.save()


class Migration(migrations.Migration):

    dependencies = [
        ('EnviTechAlApp', '0030_doccontrol_revision'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
