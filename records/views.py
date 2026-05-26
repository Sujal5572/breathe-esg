from rest_framework import generics
from .models import NormalizedRecord
from .serializers import NormalizedRecordSerializer
from django.utils import timezone


class NormalizedRecordListView(generics.ListAPIView):
    queryset = NormalizedRecord.objects.all().order_by("-created_at")
    serializer_class = NormalizedRecordSerializer


class NormalizedRecordDetailView(generics.RetrieveAPIView):
    queryset = NormalizedRecord.objects.all()
    serializer_class = NormalizedRecordSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reviews.models import ReviewDecision
from audit.models import AuditLog


class ApproveRecordView(APIView):
    def post(self, request, pk):
        try:
            record = NormalizedRecord.objects.get(pk=pk)

            if record.locked:
                return Response(
                    {"error": "Record already locked"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            record.review_status = "approved"
            record.locked = True
            record.approved_by = request.user
            record.approved_at = timezone.now()
            record.save()

            ReviewDecision.objects.create(
                normalized_record=record,
                action="approve",
                performed_by=request.user,
                comment="Approved via API",
            )

            AuditLog.objects.create(
                organization=record.organization,
                entity_type="NormalizedRecord",
                entity_id=record.id,
                action="approve",
                after_data={
                    "review_status": "approved",
                    "locked": True,
                },
                performed_by=request.user,
            )

            return Response(
                {"message": "Record approved successfully"}
            )

        except NormalizedRecord.DoesNotExist:
            return Response(
                {"error": "Record not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

class RejectRecordView(APIView):
    def post(self, request, pk):
        try:
            record = NormalizedRecord.objects.get(pk=pk)

            if record.locked:
                return Response(
                    {"error": "Approved records cannot be rejected"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            record.review_status = "rejected"
            record.save()

            ReviewDecision.objects.create(
                normalized_record=record,
                action="reject",
                performed_by=request.user,
                comment="Rejected via API",
            )

            AuditLog.objects.create(
                organization=record.organization,
                entity_type="NormalizedRecord",
                entity_id=record.id,
                action="reject",
                after_data={
                    "review_status": "rejected",
                },
                performed_by=request.user,
            )

            return Response(
                {"message": "Record rejected successfully"}
            )

        except NormalizedRecord.DoesNotExist:
            return Response(
                {"error": "Record not found"},
                status=status.HTTP_404_NOT_FOUND,
            )