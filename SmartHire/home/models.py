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

class QuestionBank(models.Model):
    id=models.AutoField(primary_key=True)
    resume=models.ForeignKey(Resume, on_delete= models.CASCADE, to_field='id')
    question = models.TextField()

class CandidateResponse(models.Model):
    id=models.AutoField(primary_key=True)
    question=models.ForeignKey(QuestionBank, on_delete= models.CASCADE, to_field='id')
    # resume=models.ForeignKey(Resume, on_delete=models.CASCADE, to_field='id')
    answer = models.TextField()
    