import uuid

from django.db import migrations, models

from history_ai.models import _new_certificate_code


def backfill_codes(apps, schema_editor):
    Certificate = apps.get_model('history_ai', 'Certificate')
    for cert in Certificate.objects.filter(code=''):
        cert.code = uuid.uuid4().hex[:10].upper()
        cert.save(update_fields=['code'])


class Migration(migrations.Migration):

    dependencies = [
        ('history_ai', '0010_review_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='code',
            field=models.CharField(default='', editable=False, max_length=12),
        ),
        migrations.RunPython(backfill_codes, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='certificate',
            name='code',
            field=models.CharField(default=_new_certificate_code, editable=False, max_length=12, unique=True),
        ),
    ]
