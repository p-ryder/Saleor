# Generated by Django 3.2.16 on 2022-12-06 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("permission", "0001_initial"),
        ("account", "0071_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="permissions",
            field=models.ManyToManyField(
                blank=True, to="permission.Permission", verbose_name="permissions"
            ),
        ),
    ]
