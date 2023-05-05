# Generated by Django 3.2.7 on 2023-05-04 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0033_auto_20230504_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='storage_choice',
            field=models.CharField(choices=[('', 'Choose...'), ('Sodium storage', 'Sodium storage'), ('Lithium Ion Battery Storage', 'Lithium Ion Battery Storage'), ('Pumped storage power plant', 'Pumped storage power plant'), ('Heat storage', 'Heat storage'), ('Gas storage', 'Gas storage'), ('Hydrogen storage', 'Hydrogen storage')], max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='year_choice_storage',
            field=models.IntegerField(choices=[('', 'Choose...'), (2025, 2025), (2030, 2030), (2035, 2035), (2040, 2040), (2045, 2045)], null=True),
        ),
    ]
