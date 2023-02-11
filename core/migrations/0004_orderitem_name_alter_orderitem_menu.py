# Generated by Django 4.1.5 on 2023-02-10 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_orderitem_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="name",
            field=models.CharField(default="Fried Rice", max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="menu",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.menu"
            ),
        ),
    ]
