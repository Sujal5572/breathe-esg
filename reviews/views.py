from rest_framework import generics

from records.models import NormalizedRecord
from records.serializers import (
    NormalizedRecordSerializer,
)


class ReviewQueueView(generics.ListAPIView):

    queryset = (
        NormalizedRecord.objects.all()
        .order_by("-created_at")
    )

    serializer_class = (
        NormalizedRecordSerializer
    )