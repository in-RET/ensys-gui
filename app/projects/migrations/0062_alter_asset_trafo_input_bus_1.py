# Generated by Django 3.2.7 on 2023-08-15 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0061_auto_20230814_1632"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="trafo_input_bus_1",
            field=models.CharField(
                choices=[("", "Choose...")], max_length=128, null=True
            ),
        ),
    ]
