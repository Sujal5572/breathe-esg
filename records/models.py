from django.db import models
from companies.models import Organization
from ingestion.models import RawRecord


class NormalizedRecord(models.Model):
    REVIEW_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="normalized_records",
    )

    raw_record = models.OneToOneField(
        RawRecord,
        on_delete=models.CASCADE,
        related_name="normalized_record",
    )

    activity_type = models.CharField(max_length=100)

    scope = models.CharField(max_length=20)

    activity_date = models.DateField()

    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    normalized_unit = models.CharField(max_length=50)

    source_unit = models.CharField(max_length=50)

    facility = models.CharField(
        max_length=255,
        blank=True,
    )

    vendor = models.CharField(
        max_length=255,
        blank=True,
    )

    suspicious = models.BooleanField(default=False)

    suspicious_reasons = models.JSONField(
        default=list,
        blank=True,
    )

    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS_CHOICES,
        default="pending",
    )

    locked = models.BooleanField(default=False)

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    approved_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.activity_type} - {self.quantity}"
    
#No edit allowed if record is locked (approved)
    def save(self, *args, **kwargs):
        if self.pk:
            existing = NormalizedRecord.objects.get(pk=self.pk)

            if existing.locked:
                raise ValueError("Approved records cannot be modified.")

        super().save(*args, **kwargs)