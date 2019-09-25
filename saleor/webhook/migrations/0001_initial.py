# Generated by Django 2.2.4 on 2019-09-25 14:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("account", "0037_delete_serviceaccounttoken")]

    operations = [
        migrations.CreateModel(
            name="Webhook",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("target_url", models.URLField(max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("secret_key", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "service_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="webhooks",
                        to="account.ServiceAccount",
                    ),
                ),
            ],
            options={"permissions": (("manage_webhooks", "Manage webhooks"),)},
        ),
        migrations.CreateModel(
            name="WebhookEvent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "event_type",
                    models.CharField(
                        db_index=True, max_length=128, verbose_name="Event type"
                    ),
                ),
                (
                    "webhook",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="webhook.Webhook",
                    ),
                ),
            ],
        ),
    ]
