# Generated by Django 4.1.5 on 2024-05-23 14:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rff_csb_project_one', '0005_vehicle_vehicle_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refill',
            old_name='type_of_refill',
            new_name='refill_type',
        ),
        migrations.RenameField(
            model_name='refill',
            old_name='vehicle',
            new_name='vehicle_id',
        ),
        migrations.AddField(
            model_name='refill',
            name='average_consumption',
            field=models.FloatField(default=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='nickname',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
