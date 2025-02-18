# Generated by Django 3.2.7 on 2023-06-06 14:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0043_remove_bus_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="inputparametersuggestion",
            name="fixed_losses_absolute_delta",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
            ),
        ),
        migrations.AddField(
            model_name="inputparametersuggestion",
            name="fixed_losses_relative_gamma",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
            ),
        ),
        migrations.AlterField(
            model_name="asset",
            name="source_choice",
            field=models.CharField(
                choices=[
                    ("", "Choose..."),
                    ("Wind", "Wind power plant"),
                    ("Photovoltaic Free Field", "Photovoltaic Free Field"),
                    ("Import Grid", "Import from the power grid"),
                    ("Other", "Other"),
                ],
                max_length=40,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="asset",
            name="storage_choice",
            field=models.CharField(
                choices=[
                    ("", "Choose..."),
                    ("Sodium storage", "Sodium storage"),
                    ("Lithium Ion Battery Storage", "Lithium Ion Battery Storage"),
                    ("Pumped storage power plant", "Pumped storage power plant"),
                    ("Heat storage", "Heat storage (seasonal)"),
                    ("Gas storage", "Gas storage"),
                    ("Hydrogen storage", "Hydrogen storage"),
                    ("Other", "Other"),
                ],
                max_length=40,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="asset",
            name="trafo_choice",
            field=models.CharField(
                choices=[
                    ("", "Choose..."),
                    ("Biogas CHP", "Biogas CHP"),
                    (
                        "Biogas injection (New facility)",
                        "Biogas injection (New facility)",
                    ),
                    ("GuD", "Gas and steam power plant"),
                    ("PtL", "Power to Liquid"),
                    ("Methanisation", "Methanisation"),
                    ("Electrolysis", "Electrolysis"),
                    ("Fuel cell", "Fuel cell"),
                    (
                        "Air source heat pump (large-scale)",
                        "Air source heat pump (large-scale)",
                    ),
                    ("Electrode heating boiler", "Electrode heating boiler"),
                    ("Other", "Other"),
                ],
                max_length=40,
                null=True,
            ),
        ),
    ]
