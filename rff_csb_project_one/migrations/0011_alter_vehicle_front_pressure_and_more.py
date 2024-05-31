# Generated by Django 4.1.5 on 2024-05-28 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rff_csb_project_one', '0010_recharge_average_consumption_recharge_notes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='front_pressure',
            field=models.FloatField(default=2.5),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='rear_pressure',
            field=models.FloatField(default=2.5),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='recommended_tire_pressure_front',
            field=models.FloatField(default=2.5),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='recommended_tire_pressure_rear',
            field=models.FloatField(default=2.5),
        ),
    ]