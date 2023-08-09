from django.db import models

# Create your models here.
class Job(models.Model):
    id=models.AutoField(primary_key=True)
    description = models.TextField()

class Resume(models.Model):
    id=models.AutoField(primary_key=True)
    job=models.ForeignKey(Job, on_delete = models.CASCADE, to_field='id')
    file = models.FileField(upload_to='allresume/', blank=True, null=True)
    shortlisted = models.BooleanField(default=False)