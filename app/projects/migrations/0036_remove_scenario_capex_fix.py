# Generated by Django 3.2.7 on 2023-05-10 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0035_auto_20230505_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario',
            name='capex_fix',
        ),
    ]
