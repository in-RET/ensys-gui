# Generated by Django 3.2.7 on 2023-08-14 16:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0055_auto_20230814_1619"),
    ]

    operations = [
        migrations.AddField(
            model_name="asset",
            name="trafo_output_conversionf_1",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="trafo_output_conversionf_2",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="trafo_output_conversionf_3",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
            ),
        ),
    ]
