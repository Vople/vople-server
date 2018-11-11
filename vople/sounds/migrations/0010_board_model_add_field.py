# Generated by Django 2.0.9 on 2018-11-01 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0009_script_plot_add_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='joined_member',
            field=models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="my_boards"),
        ),
        migrations.AddField(
            model_name='board',
            name='script',
            field=models.ForeignKey(Script, on_delete=models.DO_NOTHING, null=True, related_name="scripts"),
        ),
        migrations.AddField(
            model_name='board',
            name='mode',
            field=models.IntegerField(default=0, null=False)
        ),
        migrations.AddField(
            model_name='plot',
            name='member',
            field=models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="my_plots"),
        ),
    ]
