from rest_framework.pagination import CursorPagination


class StandardCursorPagination(CursorPagination):
    page_size = 25
    ordering = '-created_at'
    cursor_query_param = 'cursor'
