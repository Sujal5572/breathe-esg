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