from rest_framework import pagination


class RecipePagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'
