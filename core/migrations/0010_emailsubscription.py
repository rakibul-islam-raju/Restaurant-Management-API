# Generated by Django 4.1.5 on 2023-03-06 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_chef_alter_resarvation_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailSubscription",
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
                ("email", models.EmailField(max_length=254, unique=True)),
                ("subscribed_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
