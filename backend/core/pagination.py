"""
TeamTrack – Default pagination classes.
Used globally via REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'].
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """
    Page-number pagination with configurable page size.
    Query params: page, page_size (capped at max_page_size).
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """Return pagination metadata + results in a unified format."""
        return Response({
            "success": True,
            "data": {
                "results": data,
                "pagination": {
                    "count": self.page.paginator.count,
                    "total_pages": self.page.paginator.num_pages,
                    "current_page": self.page.number,
                    "page_size": self.get_page_size(self.request),
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
            },
        })
