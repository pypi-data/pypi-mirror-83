
from django.db import models

from model_search import model_search
from basement.utils import clean_code


class ServiceItemQuerySet(models.QuerySet):

    def search(
            self,
            code=None,
            category=None,
            query=None):

        queryset = self

        if category:
            queryset = queryset.filter(category=category)

        if code:
            print(clean_code(code))
            queryset = queryset.filter(code__iexact=clean_code(code))

        if query:
            queryset = model_search(query, queryset, ['name'])

        return queryset
