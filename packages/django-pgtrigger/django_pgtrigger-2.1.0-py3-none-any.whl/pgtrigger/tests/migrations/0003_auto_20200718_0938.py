# Generated by Django 3.0.7 on 2020-07-18 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_logentry_tologmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='new_field',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='logentry',
            name='old_field',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
