from django.db import models
from django.conf import settings


class Incident(models.Model):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Assigned', 'Assigned'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_incidents"
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_incidents"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_escalated = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if self.priority == "Critical":
            self.is_escalated = True
        else:
            self.is_escalated = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class IncidentLog(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="logs")
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20, blank=True, null=True)

    note = models.TextField(blank=True, null=True)  # ⭐ analyst investigation notes

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.incident.title} updated by {self.changed_by}"



