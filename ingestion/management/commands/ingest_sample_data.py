from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from companies.models import Organization
from ingestion.models import DataSource

from ingestion.services.csv_ingestion_service import ingest_csv


class Command(BaseCommand):
    help = "Ingest sample ESG data"

    def handle(self, *args, **kwargs):
        organization, _ = Organization.objects.get_or_create(
            name="Demo Enterprise"
        )

        user = User.objects.first()

        data_source, _ = DataSource.objects.get_or_create(
            organization=organization,
            source_type="sap",
            display_name="SAP Fuel Export",
        )

        batch = ingest_csv(
            file_path="sample_data/sap_fuel_sample.csv",
            organization=organization,
            data_source=data_source,
            user=user,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Ingestion completed. Batch ID: {batch.id}"
            )
        )