# Generated by Django 4.1.5 on 2023-03-11 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_alter_order_order_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_id",
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
