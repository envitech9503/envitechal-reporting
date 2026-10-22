# Clause titles in the ISO/IEC 17025 master run to ~300 characters (clause 5.3); Postgres enforces the
# varchar length, so the column is widened (23-10-2026).
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QC', '0017_internal_audit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iaclause',
            name='title',
            field=models.CharField(blank=True, default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='historicaliaclause',
            name='title',
            field=models.CharField(blank=True, default='', max_length=400),
        ),
    ]
