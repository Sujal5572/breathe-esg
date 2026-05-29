from django.db import models


class ReviewDecision(models.Model):

    ACTION_CHOICES = [
        ("approve", "Approve"),
        ("reject", "Reject"),
    ]

    normalized_record = models.ForeignKey(
        "records.NormalizedRecord",
        on_delete=models.CASCADE,
        related_name="review_decisions",
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
    )

    performed_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    comment = models.TextField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.action} - "
            f"{self.normalized_record_id}"
        )