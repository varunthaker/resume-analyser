from django.db import models

# Create your models here.
class UploadedCvData(models.Model):
    resumeFile = models.FileField(upload_to='uploads/cvs/')
    language = models.CharField(max_length=50)
    aiModel= models.CharField(max_length=50)

    def __str__(self):
        return f"CV uploaded in {self.language}"
