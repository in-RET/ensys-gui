# Generated by Django 3.2.16 on 2022-11-08 17:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("projects", "0011_capping_non_required_crate_greater_than_one")]

    operations = [
        migrations.AddField(
            model_name="asset",
            name="_max",
            field=models.FloatField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(1.0),
                ],
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="_min",
            field=models.FloatField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(1.0),
                ],
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="capex",
            field=models.FloatField(
                null=True, validators=[django.core.validators.MinValueValidator(0.0)]
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="existing",
            field=models.FloatField(
                default=None,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="maximum",
            field=models.FloatField(
                default=None,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="minimum",
            field=models.FloatField(
                default=None,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="nominal_value",
            field=models.FloatField(
                null=True, validators=[django.core.validators.MinValueValidator(0.0)]
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="nonconvex",
            field=models.BooleanField(
                choices=[(None, "Choose"), (True, "Yes"), (False, "No")],
                default=False,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="offset",
            field=models.FloatField(
                null=True, validators=[django.core.validators.MinValueValidator(0.0)]
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="opex",
            field=models.FloatField(
                null=True, validators=[django.core.validators.MinValueValidator(0.0)]
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="summed_max",
            field=models.FloatField(
                default=None,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="summed_min",
            field=models.FloatField(
                default=None,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="variable_costs",
            field=models.FloatField(
                null=True, validators=[django.core.validators.MinValueValidator(0.0)]
            ),
        ),
    ]
