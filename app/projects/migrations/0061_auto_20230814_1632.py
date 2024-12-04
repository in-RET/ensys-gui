# Generated by Django 3.2.7 on 2023-08-14 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0060_auto_20230814_1630"),
    ]

    operations = [
        migrations.AddField(
            model_name="asset",
            name="trafo_invest_bus_choice",
            field=models.CharField(choices=[], max_length=128, null=True),
        ),
        migrations.AddField(
            model_name="asset",
            name="trafo_technicalp_bus_choice",
            field=models.CharField(choices=[], max_length=128, null=True),
        ),
        migrations.AddField(
            model_name="asset",
            name="trafo_variableCosts_bus_choice",
            field=models.CharField(choices=[], max_length=128, null=True),
        ),
    ]
