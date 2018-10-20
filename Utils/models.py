from django.db import models

# Create your models here.

class Email(models.Model):
    subject = models.CharField(max_length=150)
    content = models.CharField(max_length=500)
    to = models.CharField(max_length=150)
    time = models.DateTimeField(auto_now=True)