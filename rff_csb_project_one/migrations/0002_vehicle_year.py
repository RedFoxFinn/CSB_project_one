# Generated by Django 4.1.5 on 2024-05-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rff_csb_project_one', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='year',
            field=models.IntegerField(default=2000),
        ),
    ]
