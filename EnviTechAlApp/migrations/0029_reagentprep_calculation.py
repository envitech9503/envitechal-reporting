from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("EnviTechAlApp", "0028_ppwr_custom_legend_500"),
    ]

    operations = [
        migrations.AddField(
            model_name="reagentprep",
            name="calculation",
            field=models.TextField(blank=True, default=""),
        ),
    ]
