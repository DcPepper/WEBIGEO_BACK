# Generated by Django 4.2 on 2023-05-02 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
