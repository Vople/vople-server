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
            name='script',
            field=models.ForeignKey(to='sounds.Script', on_delete=models.DO_NOTHING, related_name="my_casts")
        ),
    ]