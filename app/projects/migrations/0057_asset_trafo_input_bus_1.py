# Generated by Django 3.2.7 on 2023-08-14 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0056_auto_20230814_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='trafo_input_bus_1',
            field=models.CharField(choices=[], max_length=128, null=True),
        ),
    ]
