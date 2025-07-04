# Generated by Django 5.2.2 on 2025-06-28 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alpha', '0013_hand_special_condition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dealer',
            old_name='card_details',
            new_name='dealer_cards',
        ),
        migrations.AddField(
            model_name='dealer',
            name='face_card',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='dealer',
            name='hole_card',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
