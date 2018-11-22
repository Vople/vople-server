from django.db import migrations, models
from vople.users.models import User
from django.conf import settings
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0019_alter_fields'),
    ]
    operations = [
        migrations.AlterField(
            model_name='board',
            name='due_date',
            field=models.DateTimeField(null=True, blank=True)
        ),
        
        migrations.AlterField(
            model_name='board',
            name='present',
            field=models.ForeignKey(to='sounds.Present', on_delete=models.DO_NOTHING, null=True, blank=True),
        )
    ]