import os
import tempfile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from companies.models import Organization
from ingestion.models import DataSource
from ingestion.services.csv_ingestion_service import ingest_csv


class CSVUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response(
                {"error": "No file uploaded"},
                status=400,
            )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv",
        ) as temp_file:

            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

            temp_file_path = temp_file.name

        organization = Organization.objects.first()

        data_source = DataSource.objects.first()

        batch = ingest_csv(
            file_path=temp_file_path,
            organization=organization,
            data_source=data_source,
            user=request.user,
        )

        os.remove(temp_file_path)

        return Response({
            "message": "Upload successful",
            "batch_id": batch.id,
        })