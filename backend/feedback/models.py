from django.db import models


class GuestFeedback(models.Model):
    class Category(models.TextChoices):
        OVERALL = "overall", "Overall"
        VILLA = "villa", "Villa"
        DINING = "dining", "Dining"
        SPA = "spa", "Spa"
        ACTIVITIES = "activities", "Activities"
        STAFF = "staff", "Staff"

    category = models.CharField(max_length=32, choices=Category.choices, default=Category.OVERALL)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.get_category_display()} — {self.rating}/5"
