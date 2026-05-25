from django.db import models
from companies.models import Organization


class DataSource(models.Model):
    SOURCE_TYPES = [
        ("sap", "SAP"),
        ("utility", "Utility"),
        ("travel", "Travel"),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="data_sources",
    )

    source_type = models.CharField(
        max_length=50,
        choices=SOURCE_TYPES,
    )

    display_name = models.CharField(max_length=255)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization.name} - {self.display_name}"
    
class ImportBatch(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="import_batches",
    )

    data_source = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE,
        related_name="import_batches",
    )

    uploaded_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    filename = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    total_rows = models.IntegerField(default=0)
    failed_rows = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} ({self.status})"
    
class RawRecord(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("parsed", "Parsed"),
        ("failed", "Failed"),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="raw_records",
    )

    import_batch = models.ForeignKey(
        ImportBatch,
        on_delete=models.CASCADE,
        related_name="raw_records",
    )

    source_row_number = models.IntegerField()

    raw_payload = models.JSONField()

    parse_errors = models.JSONField(
        default=list,
        blank=True,
    )

    ingestion_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Row {self.source_row_number} - {self.ingestion_status}"