# Generated by Django 3.2.7 on 2023-03-14 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0024_auto_20230215_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='source_choice',
            field=models.CharField(choices=[('', 'Choose...'), ('wind', 'Wind power plant'), ('photovoltaic', 'Photovoltaic'), ('import_grid', 'Import from the power grid')], max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='year_choice',
            field=models.CharField(choices=[('', 'Choose...'), ('year_2025', '2025'), ('year_2030', '2030'), ('year_2035', '2035'), ('year_2040', '2040'), ('year_2045', '2045')], max_length=40, null=True),
        ),
    ]
