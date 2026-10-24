# Office-network protection per office, switchable by administrators (24-10-2026).
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


def seed(apps, schema_editor):
    ON = apps.get_model('EnviTechAlApp', 'OfficeNetwork')
    LOG = apps.get_model('EnviTechAlApp', 'OfficeNetworkLog')
    # Karachi protected; Lahore OFF - the Lahore office internet (Storm Fiber) was down on 24-10-2026 and the owner asked
    # for the Lahore restriction to be removed temporarily. An administrator turns it back ON on /office-network/.
    if not ON.objects.filter(location='Karachi').exists():
        ON.objects.create(location='Karachi', ip_address='110.93.247.168', enforced=True)
    if not ON.objects.filter(location='Lahore').exists():
        ON.objects.create(location='Lahore', ip_address='124.29.208.36', enforced=False,
                          note='Lahore office internet (Storm Fiber) down - restriction removed temporarily (owner request 24-10-2026).')
        LOG.objects.create(location='Lahore', action='off', old_value='ON', new_value='OFF',
                           reason='Lahore office internet (Storm Fiber) down - owner request 24-10-2026.', user_name='System (owner request)')


class Migration(migrations.Migration):

    dependencies = [
        ('EnviTechAlApp', '0031_doccontrol_revision_seed'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeNetwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(choices=[('Karachi', 'Karachi'), ('Lahore', 'Lahore')], max_length=20, unique=True)),
                ('ip_address', models.CharField(max_length=45)),
                ('enforced', models.BooleanField(default=True)),
                ('note', models.CharField(blank=True, default='', max_length=300)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['location']},
        ),
        migrations.CreateModel(
            name='OfficeNetworkLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=20)),
                ('action', models.CharField(max_length=10)),
                ('old_value', models.CharField(blank=True, default='', max_length=60)),
                ('new_value', models.CharField(blank=True, default='', max_length=60)),
                ('reason', models.CharField(blank=True, default='', max_length=300)),
                ('user_name', models.CharField(blank=True, default='', max_length=150)),
                ('from_ip', models.CharField(blank=True, default='', max_length=45)),
                ('at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-at', '-id']},
        ),
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
