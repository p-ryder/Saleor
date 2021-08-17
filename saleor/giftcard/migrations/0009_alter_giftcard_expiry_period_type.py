# Generated by Django 3.2.5 on 2021-08-17 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("giftcard", "0008_alter_giftcardevent_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="giftcard",
            name="expiry_period_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("day", "Day"),
                    ("week", "Week"),
                    ("month", "Month"),
                    ("year", "Year"),
                ],
                max_length=32,
                null=True,
            ),
        ),
    ]
