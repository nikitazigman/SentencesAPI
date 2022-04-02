from random import SystemRandom

from django.db.models import QuerySet
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response


class RandomModelMixin:
    def retrieve_random(self, request, *args, **kwargs):
        obj = self.get_random(
            self.filter_queryset(self.get_queryset())
        )

        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def get_random(self, queryset: QuerySet) -> QuerySet:
        if not queryset.exists():
            return get_object_or_404(queryset)

        rundom_generetor = SystemRandom()

        # ToDo: add this line to cache
        id_list = queryset.values_list("id", flat=True)
        return get_object_or_404(
            queryset, id=rundom_generetor.choice(id_list)
        )


class RetrieveRandomView(RandomModelMixin, GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.retrieve_random(request, *args, **kwargs)
