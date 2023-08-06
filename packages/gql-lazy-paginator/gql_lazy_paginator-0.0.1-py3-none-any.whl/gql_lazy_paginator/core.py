from graphene.types import (
    Int,
    List,
    Field,
    String,
    Boolean,
    Argument,
    ObjectType,
    InputObjectType,
)
from django.conf import settings

MAX_LIMIT = getattr(settings, "GQL_PAGINATION_MAX_LIMIT", 10)
MAX_PAGE_SIZE = getattr(settings, "GQL_PAGINATION_MAX_PAGE_SIZE", 20)

__all__ = [
    "PageableInputObjectType",
    "PageableInterface",
    "PaginationHelper",
    "PaginationMeta",
]


class PaginationHelper:
    """Pagination Helper"""

    @staticmethod
    def get_stops(items_count, **filters):
        page = filters.get("page", 0)
        page_size = filters.get("page_size", MAX_PAGE_SIZE)
        if page > 0:
            if page_size > MAX_PAGE_SIZE:
                page_size = MAX_PAGE_SIZE
            page -= 1
            offset = page_size * page
            limit = offset + (page_size or MAX_PAGE_SIZE)
        else:
            offset = filters.get("offset", 0)
            limit = filters.get("limit", MAX_LIMIT)
            if offset > items_count:
                return offset, limit
            if limit > MAX_LIMIT:
                limit = MAX_LIMIT
            limit += offset
        return offset, limit

    def filter(self, queryset, **filters):
        items_count = len(queryset)
        offset, limit = self.get_stops(items_count, **filters)
        return queryset[offset:limit]


class PageableInputObjectType(InputObjectType):
    """PaginationMeta InputObjectType"""

    page = Int(required=False)
    offset = Int(required=False)
    limit = Int(required=False)
    page_size = Int(required=False)


class PaginationMeta(ObjectType):
    """PaginationMeta Metadata ObjectType"""

    pages = Int()
    has_next = Boolean()
    current_page = Int(required=False)
    items_per_page = Int()
    has_previous = Boolean()
    items_count = Int()


class PageableObjects(ObjectType):

    results = List(String, filters=Argument(PageableInputObjectType))
    pagination = Field(PaginationMeta)
    data = None
    inputs = {}

    def resolve_pagination(self, info):
        filters = self.inputs.get("filters", {})
        current_page = filters.get("page", 1)
        items_per_page = filters.get("page_size", MAX_PAGE_SIZE)
        items_count = len(self.data)
        if items_count:
            pages = items_count / items_per_page
            if pages % items_per_page > 0:
                pages += 1
        else:
            pages = 0
        hide_cp = filters.get("limit") and filters.get("offset")
        return {
            "pages": pages,
            "current_page": current_page if not hide_cp else None,
            "has_next": current_page < pages,
            "has_previous": 1 < current_page < pages,
            "items_per_page": items_per_page,
            "items_count": items_count,
        }

    def resolve_results(self, info, **kwargs):
        filters = self.inputs.get("filters", {})
        paginator = PaginationHelper()
        return paginator.filter(self.data, **filters)


class PageableInterface:
    kwargs = {}
    info = None
    data = None

    def __init__(self, data, context=None, **inputs):
        self.info = context
        self.inputs = inputs
        self.data = data
