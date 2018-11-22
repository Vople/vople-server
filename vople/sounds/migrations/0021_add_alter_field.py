from django.db import migrations, models
from vople.users.models import User
from django.conf import settings
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0020_alter_second'),
    ]
    operations = [
        migrations.AlterField(
            model_name='casting',
            name='member',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, related_name="my_castings", null=True, blank=True),
        ),
        