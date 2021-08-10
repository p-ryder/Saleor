# Generated by Django 3.2.5 on 2021-08-07 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("giftcard", "0007_auto_20210719_1311"),
    ]

    operations = [
        migrations.AlterField(
            model_name="giftcardevent",
            name="type",
            field=models.CharField(
                choices=[
                    ("issued", "The gift card was created be staff user or app."),
                    ("bought", "The gift card was bought by customer."),
                    ("updated", "The gift card was updated."),
                    ("activated", "The gift card was activated."),
                    ("deactivated", "The gift card was deactivated."),
                    ("balance_reset", "The gift card balance was reset."),
                    (
                        "expiry_settings_updated",
                        "The gift card expiry settings was updated.",
                    ),
                    ("expiry_date_set", "The expiry date was set."),
                    ("sent_to_customer", "The gift card was sent to the customer."),
                    ("resent", "The gift card was resent to the customer."),
                    ("note_added", "A note was added to the gift card."),
                    ("used_in_order", "The gift card was used in order."),
                ],
                max_length=255,
            ),
        ),
    ]
