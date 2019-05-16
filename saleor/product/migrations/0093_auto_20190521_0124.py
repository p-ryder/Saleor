# Generated by Django 2.2.1 on 2019-05-21 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("product", "0092_auto_20190507_0309")]

    operations = [
        migrations.AddField(
            model_name="collectionproduct",
            name="sort_order",
            field=models.PositiveIntegerField(db_index=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name="collectionproduct",
            name="product",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="collectionproduct",
                to="product.Product",
            ),
        ),
        migrations.AlterField(
            model_name="collectionproduct",
            name="collection",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="collectionproduct",
                to="product.Collection",
            ),
        ),
        migrations.AlterModelTable(name="collectionproduct", table=None),
    ]
