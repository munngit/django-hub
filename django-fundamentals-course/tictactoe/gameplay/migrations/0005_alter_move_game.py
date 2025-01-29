# Generated by Django 5.1.4 on 2025-01-25 11:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0004_alter_move_by_first_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='game',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='move_set', to='gameplay.game'),
        ),
    ]
