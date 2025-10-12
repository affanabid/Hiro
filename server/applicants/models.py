
# Create your models here.
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Applicant(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SHORTLISTED = 'shortlisted', 'Shortlisted'
        REJECTED = 'rejected', 'Rejected'
        HIRED = 'hired', 'Hired'

    # applicant_id (unique)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=50, blank=True)

    job_applied = models.CharField(max_length=200)   # "job / Applied Position ✔"

    applied_date = models.DateField(auto_now_add=True)

    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # N/A allowed

    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    prior_experience = models.TextField(blank=True)  # free text about past companies

    source = models.CharField(max_length=120, blank=True)  # optional

    # Skill set (array of strings in Postgres)
    skills = ArrayField(
        base_field=models.CharField(max_length=80),
        blank=True,
        default=list
    )

    def __str__(self):
        return f"{self.name} — {self.job_applied}"
