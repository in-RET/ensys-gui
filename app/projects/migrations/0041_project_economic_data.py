# Generated by Django 3.2.7 on 2023-05-16 19:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0040_remove_project_economic_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="economic_data",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="projects.economicdata",
            ),
        ),
    ]
