from .logic.random_view import RetrieveRandomView
from .models import Quote
from .serializers import QuoteSerializer


class RandomQuoteView(RetrieveRandomView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    filterset_fields = ["category", "author"]
