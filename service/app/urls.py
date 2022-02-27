from django.urls import path
from . import views

urlpatterns = [
    path("content/", views.ContentList.as_view(), name="content"),
]
