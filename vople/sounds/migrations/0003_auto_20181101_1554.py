# Generated by Django 2.0.9 on 2018-11-01 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0002_auto_20181101_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='board',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
