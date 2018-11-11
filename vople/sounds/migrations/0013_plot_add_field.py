from django.db import migrations, models
from vople.users.models import User
from django.conf import settings
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0012_auto_20181112_0407'),
    ]

    operations = [
        migrations.AddField(
            model_name='plot',
            name='comment',
            field=models.ForeignKey(on_delete=models.DO_NOTHING, null=True, related_name="my_boards", to='sounds.Comment'),
        ),
        migrations.AddField(
            model_name='plot',
            name='is_adjust',
            field=models.BooleanField(null=False, default=False)
        ),
        migrations.AddField(
            model_name='plot',
            name='roll_name',
            field=models.CharField(null=False, default="Roll_Name", max_length=80),
        ),
        migrations.AddField(
            model_name='plot',
            name='order',
            field=models.IntegerField(null=False, default=0)
        ),
    ]
