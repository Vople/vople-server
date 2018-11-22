from django.db import migrations, models
from vople.users.models import User
from django.conf import settings
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('sounds', '0022_add_commenting_model'),
    ]
    
    operations = [
        migrations.AddField(
            model_name='cast',
            name='script_title',
            field=script_title = models.CharField(max_length=30, blank=True)
        ),
    ]