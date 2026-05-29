from django.urls import path

from .views import (
    NormalizedRecordListView,
    NormalizedRecordDetailView,
    ApproveRecordView,
    RejectRecordView,
)

urlpatterns = [
    path(
        "records/",
        NormalizedRecordListView.as_view(),
    ),

    path(
        "records/<int:pk>/",
        NormalizedRecordDetailView.as_view(),
    ),

    path(
        "records/<int:pk>/approve/",
        ApproveRecordView.as_view(),
    ),

    path(
        "records/<int:pk>/reject/",
        RejectRecordView.as_view(),
    ),
]