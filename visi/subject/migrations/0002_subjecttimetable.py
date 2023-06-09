# Generated by Django 4.1.8 on 2023-04-15 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("teacher", "0001_initial"),
        ("subject", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubjectTimetable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField(verbose_name="start time")),
                ("end_time", models.DateTimeField(verbose_name="end time")),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="subject.subject",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="teacher.teacher",
                    ),
                ),
            ],
        ),
    ]
