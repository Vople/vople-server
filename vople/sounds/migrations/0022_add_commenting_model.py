from django.db import migrations, models
from vople.users.models import User
from django.conf import settings
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('sounds', '0021_auto_20181122_2223'),
    ]
    
    operations = [
        migrations.CreateModel(
            name='Commenting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.ForeignKey(on_delete=models.CASCADE, related_name="commentings", to='sounds.Board')),
                ('comment', models.ForeignKey(blank=True, on_delete=models.CASCADE, to='sounds.Comment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='plot',
            name='comment',
            model=models.ForeignKey(to='sounds.Commenting', on_delete=models.CASCADE, null=True, blank=True)
        ),
        migrations.AddField(
            model_name='casting',
            name='board',
            field=models.ForeignKey(to='sounds.Board', on_delete=models.CASCADE, related_name="castings")
        ),
        
    ]