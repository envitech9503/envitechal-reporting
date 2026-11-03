from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("QC", "0025_soc_legends"),
    ]

    operations = [
        migrations.CreateModel(
            name="RdsDraft",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("kind", models.CharField(max_length=2)),
                ("page", models.CharField(max_length=10)),
                ("sample_id", models.CharField(max_length=200)),
                ("payload", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="rds_drafts", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-updated_at",), "unique_together": {("user", "kind", "page", "sample_id")}},
        ),
    ]
