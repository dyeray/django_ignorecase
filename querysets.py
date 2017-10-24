from django.core.exceptions import FieldDoesNotExist
from django.db.models import Field, QuerySet

from .fields import IgnoreCaseMixin
from .tools import safe_traverse


class IQuerySet(QuerySet):

    def __get_field(self, path) -> Field:
        """
        Traverse the relations on a query until reaching the last field if it exists.

        :param path: ORM path (ex: user__vehicle__license).
        :return: Field on the leaf of the path (if it exists).
        """
        model = self.model
        path_nodes = path.split('__')
        for node in path_nodes:
            try:
                field = model._meta.get_field(node)
            except (FieldDoesNotExist, AttributeError):
                return None
            model = safe_traverse(field, 'rel', 'to')
        return field

    def filter(self, *args, **kwargs):
        """Override filter call to ignore case on case agnostic fields."""
        for key, value in kwargs.items():
            field = self.__get_field(key)
            if isinstance(field, IgnoreCaseMixin) and value is not None:
                kwargs[key] = value.lower()
        return super().filter(*args, **kwargs)
