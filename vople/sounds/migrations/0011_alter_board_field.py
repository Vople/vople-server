# Generated by Django 2.0.9 on 2018-11-01 16:39

from django.db import migrations, models
from vople.users.models import User
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0010_board_model_add_field'),
    ]

    operations = [
        migrations.AlterField(
        model_name='Board',
        name='joined_member',
        field=models.ManyToManyField(on_delete=models.DO_NOTHING, null=True, to=settings.AUTH_USER_MODEL),
    ),
    ]
