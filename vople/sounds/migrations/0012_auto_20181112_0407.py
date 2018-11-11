from django.db import migrations, models
from vople.users.models import User
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0011_alter_board_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='content',
            field=models.TextField(default='_REMOVE_'),
        ),
        migrations.AlterField(
            model_name='board',
            name='joined_member',
            field=models.ManyToManyField(null=True, related_name='my_boards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='board',
            name='title',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='boardlike',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='board_likes', to='sounds.Board'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='sounds.Board'),
        ),
        migrations.AlterField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comment_likes', to='sounds.Comment'),
        ),
        migrations.AlterField(
            model_name='plot',
            name='script',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='plots', to='sounds.Script'),
        ),
        migrations.AlterField(
            model_name='script',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]