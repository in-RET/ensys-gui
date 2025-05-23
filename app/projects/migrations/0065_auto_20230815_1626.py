# Generated by Django 3.2.7 on 2023-08-15 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0064_alter_asset_trafo_input_bus_1"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="trafo_input_bus_2",
            field=models.CharField(default="Choose", max_length=128),
        ),
        migrations.AlterField(
            model_name="asset",
            name="trafo_input_bus_3",
            field=models.CharField(default="Choose", max_length=128),
        ),
        migrations.AlterField(
            model_name="asset",
            name="trafo_invest_bus_choice",
            field=models.CharField(default="Choose", max_length=128),
        ),
        migrations.AlterField(
            model_name="asset",
            name="trafo_output_bus_1",
            field=models.CharField(default="Choose", max_length=128),
        ),
        migrations.AlterField(
            model_name="asset",
            name="trafo_output_bus_2",
            field=models.CharField(default="Choose", max_length=128),
        ),
        migrations.AlterField(
            model_name="asset",
            name="trafo_output_bus_3",
            field=models.CharField(default="Choose", max_length=128),
        ),
        migrations.AlterField(
            model_name="asset",
            name="trafo_technicalp_bus_choice",
            field=models.CharField(default="Choose", max_length=128),
        ),
        migrations.AlterField(
            model_name="asset",
            name="trafo_variableCosts_bus_choice",
            field=models.CharField(default="Choose", max_length=128),
        ),
    ]
