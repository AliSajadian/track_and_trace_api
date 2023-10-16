# Generated by Django 4.2.5 on 2023-10-14 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Weather",
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
                ("zip_code", models.CharField(max_length=10, unique=True)),
                ("country", models.CharField(max_length=50)),
                ("city", models.CharField(max_length=50)),
                ("weather_description", models.CharField(max_length=20)),
                ("temperature", models.FloatField()),
                ("wind_speed", models.FloatField()),
                ("retrieved_on", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "tbl_weather", "ordering": ["-retrieved_on"],},
        ),
    ]
