# Generated by Django 5.2.2 on 2025-06-21 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alpha', '0006_alter_hand_hand_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hand',
            name='hand_id',
            field=models.IntegerField(default=0),
        ),
    ]
