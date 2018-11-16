
from django.db import migrations, models
from vople.users.models import User
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0017_auto_20181116_1311'),
    ]
    operations = [
        migrations.AlterField(
            model_name='board',
            name='script',
            field=models.ForeignKey(to='sounds.Script', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="scripts"),
        ),
        migrations.AlterField(
            model_name='board',
            name='present',
            field=models.ForeignKey(to='sounds.Present', on_delete=models.DO_NOTHING, null=True, blank=True)
        ),
        
    ]