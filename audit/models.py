from django.db import models
from companies.models import Organization


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("create", "Create"),
        ("update", "Update"),
        ("approve", "Approve"),
        ("reject", "Reject"),
        ("lock", "Lock"),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )

    entity_type = models.CharField(max_length=100)

    entity_id = models.IntegerField()

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES,
    )

    before_data = models.JSONField(
        null=True,
        blank=True,
    )

    after_data = models.JSONField(
        null=True,
        blank=True,
    )

    performed_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.entity_type} - {self.action}"