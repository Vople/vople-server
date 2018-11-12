# Generated by Django 2.0.9 on 2018-11-01 16:39

from django.db import migrations, models
from vople.users.models import User
from django.conf import settings
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0015_cast_add_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cast',
            name='member',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, related_name="my_casts", null=True),
        ),
        migrations.AlterField(
            model_name='cast',
            name='script',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.DO_NOTHING, to='sounds.Script', related_name="casts"),
        ),
    ]