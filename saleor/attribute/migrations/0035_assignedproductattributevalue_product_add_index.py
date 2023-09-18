# Generated by Django 3.2.20 on 2023-08-24 11:25

from django.db import migrations
from django.contrib.postgres.operations import AddIndexConcurrently
from django.contrib.postgres.indexes import BTreeIndex


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("attribute", "0034_assignedpageattributevalue_page_data_migration"),
    ]

    operations = [
        # We have introduced a non-concurrent index creation in one of previous
        # migrations. This has only been applied to dev environments of people
        # who work on the main branch.
        migrations.RunSQL(
            """
                DROP INDEX attribute_assignedproductattributevalue_product_id_805656f1
                ON attribute_assignedproductattributevalue;
            """
        ),
        AddIndexConcurrently(
            model_name="assignedproductattributevalue",
            index=BTreeIndex(
                fields=["product"], name="assignedprodattrval_product_idx"
            ),
        ),
    ]
