# Generated by Django 5.1.4 on 2025-01-25 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0005_alter_move_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='by_first_player',
            field=models.BooleanField(editable=False, null=True),
        ),
    ]
