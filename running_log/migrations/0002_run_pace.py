# Generated by Django 4.1.10 on 2023-07-26 01:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("running_log", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="run",
            name="pace",
            field=models.FloatField(default=15),
            preserve_default=False,
        ),
    ]