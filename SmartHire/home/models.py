from django.db import models

# Create your models here.
class Resume(models.Model):
    # Other fields for your model, if any
    # ...

    # FileField to store multiple files
    files = models.FileField(upload_to='allresume/', blank=True, null=True)