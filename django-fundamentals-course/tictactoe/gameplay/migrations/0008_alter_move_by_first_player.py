# Generated by Django 5.1.4 on 2025-02-01 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0007_alter_move_x_alter_move_y'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='by_first_player',
            field=models.BooleanField(default=False, editable=False),
            preserve_default=False,
        ),
    ]
