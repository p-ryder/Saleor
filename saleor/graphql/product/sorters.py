import graphene
from django.db.models import Count, QuerySet

from ..core.types import SortInputObjectType


class CollectionOrderField(graphene.Enum):
    NAME = "name"
    AVAILABILITY = "is_published"
    PRODUCT_COUNT = "product_count"

    @property
    def description(self):
        # pylint: disable=no-member
        if self in [
            CollectionOrderField.NAME,
            CollectionOrderField.AVAILABILITY,
            CollectionOrderField.PRODUCT_COUNT,
        ]:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort collections by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)

    @staticmethod
    def sort_by_product_count(queryset: QuerySet, sort_by: dict):
        return queryset.annotate(product_count=Count("collectionproduct__id")).order_by(
            f"{sort_by.direction}product_count", "slug"
        )


class CollectionOrder(SortInputObjectType):
    class Meta:
        sort_enum = CollectionOrderField
        type_name = "collection"


class ProductOrderField(graphene.Enum):
    NAME = "name"
    PRICE = "price_amount"
    MINIMAL_PRICE = "minimal_variant_price_amount"
    DATE = "updated_at"
    TYPE = "product_type__name"
    PUBLISHED = "is_published"

    @property
    def description(self):
        # pylint: disable=no-member
        descrtiptions = {
            ProductOrderField.NAME.name: "name",
            ProductOrderField.PRICE.name: "price",
            ProductOrderField.TYPE.name: "type",
            ProductOrderField.MINIMAL_PRICE.name: (
                "a minimal price of a product's variant"
            ),
            ProductOrderField.DATE.name: "update date",
            ProductOrderField.PUBLISHED.name: "publication status",
        }
        if self.name in descrtiptions:
            return f"Sort products by {descrtiptions[self.name]}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class ProductOrder(SortInputObjectType):
    attribute_id = graphene.Argument(
        graphene.ID,
        description=(
            "Sort product by the selected attribute's values.\n"
            "Note: this doesn't take translations into account yet."
        ),
    )

    class Meta:
        sort_enum = ProductOrderField
        type_name = "product"
