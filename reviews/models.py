from django.db import models
from records.models import NormalizedRecord


class ReviewDecision(models.Model):
    ACTION_CHOICES = [
        ("approve", "Approve"),
        ("reject", "Reject"),
        ("request_changes", "Request Changes"),
    ]

    normalized_record = models.ForeignKey(
        NormalizedRecord,
        on_delete=models.CASCADE,
        related_name="review_decisions",
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES,
    )

    comment = models.TextField(
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
        return f"{self.action} - {self.normalized_record.id}"