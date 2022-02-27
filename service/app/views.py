from rest_framework import generics

from .models import Content
from .serializers import ContentSerializer


class ContentList(generics.ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def get(self, request, *args, **kwargs):
        print(f"HEY: {request.user.id=}")
        return super().get(request, *args, **kwargs)
