
from django.db import migrations, models
from vople.users.models import User
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0013_plot_add_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='member',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, related_name="my_plots", blank=True),
        ),
        migrations.AlterField(
            model_name='plot',
            name='comment',
            field=models.ForeignKey(to='sounds.Comment', on_delete=models.DO_NOTHING, null=True, related_name="comment_plots", blank=True)
        ),
        
    ]