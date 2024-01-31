# Generated by Django 3.2 on 2022-04-04 19:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("projects", "0001_initial"), ("dashboard", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="sensitivityanalysisgraph",
            name="analysis",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="projects.sensitivityanalysis",
            ),
        ),
        migrations.AddField(
            model_name="reportitem",
            name="simulations",
            field=models.ManyToManyField(to="projects.Simulation"),
        ),
        migrations.AddField(
            model_name="kpiscalarresults",
            name="simulation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="projects.simulation"
            ),
        ),
        migrations.AddField(
            model_name="kpicostsmatrixresults",
            name="simulation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="projects.simulation"
            ),
        ),
        migrations.AddField(
            model_name="assetsresults",
            name="simulation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="projects.simulation"
            ),
        ),
    ]
