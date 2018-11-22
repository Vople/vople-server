from django.db import migrations, models
from vople.users.models import User
from django.conf import settings
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0019_alter_fields'),
    ]
    operations = [
        migrations.RemoveField(
            model_name='casting',
            name='created_at',
        )
        migrations.RemoveField(
            model_name='casting',
            name='updated_at',
        )
    ]