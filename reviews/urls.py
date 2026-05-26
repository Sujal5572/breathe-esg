from django.urls import path
from .views import ReviewQueueView

urlpatterns = [
    path(
        "records/",
        ReviewQueueView.as_view(),
    ),
]