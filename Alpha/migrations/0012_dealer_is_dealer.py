# Generated by Django 5.2.2 on 2025-06-23 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alpha', '0011_dealer'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='is_dealer',
            field=models.BooleanField(default=True),
        ),
    ]
