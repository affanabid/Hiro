from django.db import models



# / → Job list

# /job/create/ → Add new

# /job/<id>/ → Detail

# /job/<id>/update/ → Edit

# /job/<id>/delete/ → Delete

class Job(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('paused', 'Paused'),
    ]
    JOB_TYPE_CHOICES = [
        ('onsite', 'Onsite'),
        ('remote', 'Remote'),
    ]
    JOB_TIME_CHOICES = [
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    date = models.DateField(auto_now_add=True)
    jobtype = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    jobtime = models.CharField(max_length=20, choices=JOB_TIME_CHOICES)
    shift = models.CharField(max_length=50, blank=True, null=True)
    required_skills = models.TextField()
    domain = models.CharField(max_length=100, blank=True, null=True)

    def total_applicants(self):
        return self.applicants.count()

    def __str__(self):
        return self.title
