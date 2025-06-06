# Generated by Django 3.2.7 on 2023-08-15 17:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0067_auto_20230815_1638"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="trafo_invest_bus_choice",
            field=models.CharField(
                blank=True, default="Choose", max_length=128, null=True
            ),
        ),
        migrations.AlterField(
            model_name="asset",
            name="trafo_output_conversionf_1",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
            ),
        ),
        migrations.AlterField(
            model_name="asset",
            name="trafo_technicalp_bus_choice",
            field=models.CharField(
                blank=True, default="Choose", max_length=128, null=True
            ),
        ),
        migrations.AlterField(
            model_name="asset",
            name="trafo_variableCosts_bus_choice",
            field=models.CharField(
                blank=True, default="Choose", max_length=128, null=True
            ),
        ),
    ]
