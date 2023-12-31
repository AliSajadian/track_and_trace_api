# Generated by Django 4.2.5 on 2023-10-14 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
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
                ("name", models.CharField(max_length=50, unique=True)),
                ("price", models.FloatField(null=True)),
                ("sku", models.CharField(max_length=8)),
            ],
            options={"db_table": "tbl_article",},
        ),
        migrations.CreateModel(
            name="Carrier",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
            options={"db_table": "tbl_carrier",},
        ),
        migrations.CreateModel(
            name="Customer",
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
                ("country", models.CharField(max_length=50)),
                ("city", models.CharField(max_length=50)),
                ("zip_code", models.CharField(max_length=5)),
                ("street", models.CharField(max_length=50)),
            ],
            options={"db_table": "tbl_customer",},
        ),
        migrations.CreateModel(
            name="Shop",
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
                ("country", models.CharField(max_length=50)),
                ("city", models.CharField(max_length=50)),
                ("zip_code", models.CharField(max_length=5)),
                ("street", models.CharField(max_length=50)),
            ],
            options={"db_table": "tbl_shop",},
        ),
        migrations.CreateModel(
            name="Shipment",
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
                ("tracking_number", models.CharField(max_length=10)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("in-transit", "In Transit"),
                            ("inbound-scan", "Inbound Scan"),
                            ("delivery", "Delivery"),
                            ("transit", "Transit"),
                            ("scanned", "Scanned"),
                        ],
                        default="in-transit",
                        max_length=12,
                    ),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shipments",
                        to="shipment.customer",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shipments",
                        to="shipment.shop",
                    ),
                ),
            ],
            options={"db_table": "tbl_shipment",},
        ),
        migrations.AddField(
            model_name="customer",
            name="shops",
            field=models.ManyToManyField(
                related_name="customers",
                through="shipment.Shipment",
                to="shipment.shop",
            ),
        ),
        migrations.CreateModel(
            name="ArticleShipment",
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
                ("quantity", models.PositiveSmallIntegerField()),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="articles",
                        to="shipment.article",
                    ),
                ),
                (
                    "shipment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shipments",
                        to="shipment.shipment",
                    ),
                ),
            ],
            options={"db_table": "tbl_article_shipment",},
        ),
        migrations.AddField(
            model_name="article",
            name="shipments",
            field=models.ManyToManyField(
                related_name="articles",
                through="shipment.ArticleShipment",
                to="shipment.shipment",
            ),
        ),
    ]
