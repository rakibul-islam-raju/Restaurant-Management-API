# Generated by Django 4.1.5 on 2023-03-09 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_emailsubscription"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="emailsubscription",
            options={"ordering": ["-id"]},
        ),
        migrations.AddField(
            model_name="order",
            name="order_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]