from django.urls import path

from .views import RandomQuoteView

urlpatterns = [
    path(
        "random_quote", RandomQuoteView.as_view(), name="random_quote"
    ),
]
