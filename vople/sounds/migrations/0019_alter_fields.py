from django.db import migrations, models
from vople.users.models import User
from django.conf import settings
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0018_alter_board_model'),
    ]
    operations = [
        migrations.CreateModel(
            name='Casting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('script', models.ForeignKey(on_delete=models.CASCADE, to='sounds.Script')),
                ('cast', models.ForeignKey(on_delete=models.CASCADE, to='sounds.Cast')),
                ('member', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, related_name="my_casts")),
                ('is_adjust', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='cast',
            name='is_adjust',
        ),
        migrations.RemoveField(
            model_name='cast',
            name='member',
        ),
        migrations.RemoveField(
            model_name='cast',
            name='script',
        ),
        migrations.AddField(
            model_name='script',
            name='casts',
            field=models.ManyToManyField(to='sounds.Cast', through='Casting', thorugh_fields=('script', 'cast'), related_name='scripts'),
        ),
        
    ]